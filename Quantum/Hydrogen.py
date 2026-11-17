import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, CheckButtons
from matplotlib.colors import hsv_to_rgb
from scipy.special import sph_harm_y, genlaguerre
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from functools import lru_cache


# =============================================
#  Konstanten & Hilfsfunktionen
# =============================================

a0 = 1  # Bohr-Radius (atomare Einheiten)


@lru_cache(maxsize=64)
def _factorial(k):
    return math.factorial(k)


def energy_n(n_q):
    """Energie: E_n = -1/(2n^2) [a.u.]"""
    return -0.5 / (n_q * n_q)


def hydrogen_psi(n_q, l_q, m_q, r, theta, phi):
    """Psi_nlm(r, theta, phi) - komplexwertig."""
    norm = np.sqrt(
        (2 / (n_q * a0)) ** 3
        * _factorial(n_q - l_q - 1)
        / (2 * n_q * _factorial(n_q + l_q))
    )
    rho = 2 * r / (n_q * a0)
    L = genlaguerre(n_q - l_q - 1, 2 * l_q + 1)(rho)
    Y_lm = sph_harm_y(l_q, m_q, theta, phi)
    return norm * np.exp(-r / (n_q * a0)) * rho ** l_q * L * Y_lm


def psi_at_points(states, points, t=0.0):
    """Psi(r, t) = sum c_i psi_i(r) exp(-i E_i t) an Punkten (N, 3)."""
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    r = np.sqrt(x * x + y * y + z * z)
    r_safe = np.where(r == 0, 1e-30, r)
    theta = np.arccos(np.clip(z / r_safe, -1, 1))
    phi = np.arctan2(y, x)
    psi = np.zeros(len(points), dtype=complex)
    norm = np.sqrt(sum(abs(c_i) ** 2 for _, _, _, c_i in states))
    if norm < 1e-30:
        return psi
    for n_q, l_q, m_q, c_i in states:
        psi_i = hydrogen_psi(n_q, l_q, m_q, r, theta, phi)
        psi += (c_i / norm) * psi_i * np.exp(-1j * energy_n(n_q) * t)
    return psi


# =============================================
#  Isosurface
# =============================================

def compute_isosurface(rho, coords, einschluss=0.5, max_faces=50000):
    """Marching Cubes auf rho = |Psi|^2.  Returns (verts, faces) oder (None, None)."""
    rho = np.clip(rho, 0, None)
    dx = coords[1] - coords[0]
    dV = dx ** 3
    total = rho.sum() * dV
    if total <= 0:
        return None, None
    level = _find_threshold(rho, dV, total, einschluss)
    if level <= 0:
        return None, None
    step = 2 if len(coords) > 60 else 1
    try:
        verts, faces, _, _ = marching_cubes(
            rho, level=level, spacing=(dx, dx, dx), step_size=step
        )
    except (ValueError, RuntimeError):
        return None, None
    verts += coords[0]
    if len(faces) > max_faces:
        idx = np.linspace(0, len(faces) - 1, max_faces, dtype=int)
        faces = faces[idx]
    return verts, faces


def _find_threshold(rho, dV, total, einschluss, n_bins=1000):
    flat = rho.ravel()
    rho_max = flat.max()
    if rho_max <= 0:
        return 0.0
    edges = np.linspace(0, rho_max, n_bins + 1)
    bi = np.clip(np.searchsorted(edges, flat, side="right") - 1, 0, n_bins - 1)
    bp = np.zeros(n_bins)
    np.add.at(bp, bi, flat)
    bp *= dV
    cum = np.cumsum(bp[::-1])[::-1]
    idx = np.searchsorted(-cum, -einschluss * total)
    return edges[min(idx, n_bins - 1)]


# =============================================
#  Phasenfarben
# =============================================

def phase_to_rgba(psi_vals, alpha=0.7):
    """arg(Psi) -> RGBA ueber HSV (zyklisch)."""
    hue = (np.angle(psi_vals) + np.pi) / (2 * np.pi)
    hsv = np.stack([hue, np.full_like(hue, 0.9), np.ones_like(hue)], axis=-1)
    rgb = hsv_to_rgb(hsv)
    rgba = np.empty((*rgb.shape[:-1], 4))
    rgba[..., :3] = rgb
    rgba[..., 3] = alpha
    return rgba


# =============================================
#  Simulation
# =============================================

class Simulation:
    def __init__(self):
        # Superposition: [(n, l, m, complex_coeff), ...]
        self.states = [(2, 1, 0, 1.0 + 0j)]

        # Slider-Werte fuer naechsten Zustand
        self.cur_n, self.cur_l, self.cur_m = 2, 1, 0

        # Gitter
        self.aufloesung = 40
        self.einschluss = 0.5
        self.extent = 10
        self.coords = None

        # Darstellung
        self.show_phase = True
        self.animating = False
        self.time = 0.0
        self.dt = 0.3  # Zeitschritt pro Frame [a.u.]

        # Gecachte Daten
        self._psi_spatial = {}  # (n,l,m) -> 3D complex array
        self.verts = None
        self.faces = None
        self.anim = None

        self._build_gui()
        self._full_recompute()
        plt.show()

    # == GUI ==========================================
    def _build_gui(self):
        self.fig = plt.figure(figsize=(15, 9), facecolor="#1a1a2e")
        self.fig.suptitle(
            "Hydrogen-Orbital  \u00b7  Phase & Superposition",
            color="white", fontsize=14, fontweight="bold", y=0.98,
        )
        self.ax3d = self.fig.add_axes(
            [0.01, 0.05, 0.58, 0.88], projection="3d"
        )
        self._style_ax(self.ax3d)

        C, W = 0.63, 0.24

        # -- n / l / m --
        self.sl_n = self._mk_slider(C, 0.90, W, "n", 1, 7, self.cur_n, 1, "#16c79a")
        self.sl_l = self._mk_slider(
            C, 0.86, W, "l", 0, max(self.cur_n - 1, 0), self.cur_l, 1, "#16c79a"
        )
        self.sl_m = self._mk_slider(
            C, 0.82, W, "m", -self.cur_l, max(self.cur_l, 0), self.cur_m, 1, "#16c79a"
        )
        self.sl_n.on_changed(self._on_n)
        self.sl_l.on_changed(self._on_l)
        self.sl_m.on_changed(self._on_m)

        # -- +Zustand / Zuruecksetzen --
        hw = W / 2 - 0.005
        self.btn_add = self._mk_button(
            C, 0.76, hw, 0.04, "+ Zustand", "#16c79a", "#12a87e"
        )
        self.btn_clr = self._mk_button(
            C + hw + 0.01, 0.76, hw, 0.04, "Zur\u00fccksetzen", "#e94560", "#c73652"
        )
        self.btn_add.on_clicked(self._on_add)
        self.btn_clr.on_clicked(self._on_clear)

        # -- Zustandsliste --
        self.ax_list = self.fig.add_axes([C, 0.60, W, 0.13], facecolor="#0f0f1a")
        self.ax_list.set_xticks([])
        self.ax_list.set_yticks([])
        self.ax_list.set_title("Superposition", color="white", fontsize=9, pad=4)
        for sp in self.ax_list.spines.values():
            sp.set_color("#333")
        self._update_list_text()

        # -- Einschluss / Aufloesung --
        self.sl_enc = self._mk_slider(
            C, 0.54, W, "Einschluss", 0.1, 0.95, self.einschluss, 0.05, "#e94560"
        )
        self.sl_res = self._mk_slider(
            C, 0.50, W, "Aufl\u00f6sung", 20, 80, self.aufloesung, 5, "#0f3460"
        )
        self.sl_enc.on_changed(lambda v: setattr(self, "einschluss", float(v)))
        self.sl_res.on_changed(lambda v: setattr(self, "aufloesung", int(v)))

        # -- Berechnen --
        self.btn_calc = self._mk_button(
            C, 0.43, W, 0.05, "\u25b6  Berechnen", "#e94560", "#c73652"
        )
        self.btn_calc.on_clicked(self._on_calc)

        # -- Checkboxen --
        ax_chk = self.fig.add_axes([C, 0.30, W, 0.10], facecolor="#0f0f1a")
        self.checks = CheckButtons(
            ax_chk,
            ["Phase anzeigen", "Animation"],
            actives=[True, False],
        )
        for lb in self.checks.labels:
            lb.set_color("white")
            lb.set_fontsize(9)
        self.checks.on_clicked(self._on_check)

        # -- Geschwindigkeit --
        self.sl_spd = self._mk_slider(
            C, 0.24, W, "Geschw.", 0.05, 2.0, self.dt, 0.05, "#0f3460"
        )
        self.sl_spd.on_changed(lambda v: setattr(self, "dt", float(v)))

    # -- Slider-Helper --
    def _mk_slider(self, left, bottom, width, label, lo, hi, init, step, col):
        ax = self.fig.add_axes([left, bottom, width, 0.025], facecolor="#0f0f1a")
        s = Slider(ax, label, lo, hi, valinit=init, valstep=step, color=col)
        s.label.set_color("white")
        s.valtext.set_color("white")
        return s

    # -- Button-Helper --
    def _mk_button(self, left, bottom, width, height, text, col, hov):
        ax = self.fig.add_axes([left, bottom, width, height], facecolor="#0f0f1a")
        btn = Button(ax, text, color=col, hovercolor=hov)
        btn.label.set_color("white")
        btn.label.set_fontsize(9)
        return btn

    # == Events =======================================
    def _on_n(self, val):
        self.cur_n = int(val)
        lmax = self.cur_n - 1
        self.sl_l.valmax = lmax
        self.sl_l.ax.set_xlim(0, max(lmax, 1))
        if self.cur_l > lmax:
            self.sl_l.set_val(lmax)

    def _on_l(self, val):
        self.cur_l = int(val)
        self.sl_m.valmin = -self.cur_l
        self.sl_m.valmax = self.cur_l
        self.sl_m.ax.set_xlim(-max(self.cur_l, 1), max(self.cur_l, 1))
        if abs(self.cur_m) > self.cur_l:
            self.sl_m.set_val(0)

    def _on_m(self, val):
        self.cur_m = int(val)

    def _on_add(self, _):
        key = (self.cur_n, self.cur_l, self.cur_m)
        for i, (ni, li, mi, ci) in enumerate(self.states):
            if (ni, li, mi) == key:
                self.states[i] = (ni, li, mi, ci + 1.0)
                self._update_list_text()
                return
        self.states.append((*key, 1.0 + 0j))
        self._update_list_text()

    def _on_clear(self, _):
        self.states = [(self.cur_n, self.cur_l, self.cur_m, 1.0 + 0j)]
        self.time = 0.0
        self._update_list_text()
        self._full_recompute()

    def _on_calc(self, _):
        self._full_recompute()

    def _on_check(self, label):
        if label == "Phase anzeigen":
            self.show_phase = not self.show_phase
            self._redraw()
        elif label == "Animation":
            self.animating = not self.animating
            if self.animating:
                self._start_anim()
            else:
                self._stop_anim()

    def _update_list_text(self):
        self.ax_list.cla()
        self.ax_list.set_xticks([])
        self.ax_list.set_yticks([])
        self.ax_list.set_title("Superposition", color="white", fontsize=9, pad=4)
        for sp in self.ax_list.spines.values():
            sp.set_color("#333")
        # Normierte Koeffizienten anzeigen
        norm = np.sqrt(sum(abs(ci) ** 2 for _, _, _, ci in self.states))
        parts = []
        for ni, li, mi, ci in self.states:
            cn = ci / norm if norm > 1e-30 else ci
            cs = f"{cn.real:.2f}" if abs(cn.imag) < 1e-10 else f"({cn:.2f})"
            parts.append(f"{cs}\u00b7|{ni},{li},{mi}\u27e9")
        txt = " + ".join(parts) if parts else "(leer)"
        self.ax_list.text(
            0.05, 0.5, f"\u03a8 = {txt}",
            transform=self.ax_list.transAxes,
            color="white", fontsize=8, va="center", wrap=True,
        )

    # == Berechnung ===================================
    def _full_recompute(self):
        """Raeumliche Wellenfunktionen & Isoflaeche neu berechnen."""
        max_n = max(s[0] for s in self.states)
        self.extent = max(2 * max_n ** 2, 10)
        self.coords = np.linspace(-self.extent, self.extent, self.aufloesung)

        X, Y, Z = np.meshgrid(self.coords, self.coords, self.coords, indexing="ij")
        r = np.sqrt(X * X + Y * Y + Z * Z)
        r_safe = np.where(r == 0, 1e-30, r)
        theta = np.arccos(np.clip(Z / r_safe, -1, 1))
        phi = np.arctan2(Y, X)

        self._psi_spatial = {}
        for n_q, l_q, m_q, _ in self.states:
            key = (n_q, l_q, m_q)
            if key not in self._psi_spatial:
                self._psi_spatial[key] = hydrogen_psi(n_q, l_q, m_q, r, theta, phi)

        self._recompute_surface()
        self._redraw()

    def _psi_grid(self, t):
        """Psi(r, t) auf dem Gitter (normiert: sum|c_i|^2 = 1)."""
        psi = np.zeros_like(next(iter(self._psi_spatial.values())), dtype=complex)
        norm = np.sqrt(sum(abs(c_i) ** 2 for _, _, _, c_i in self.states))
        if norm < 1e-30:
            return psi
        for n_q, l_q, m_q, c_i in self.states:
            psi += (
                (c_i / norm)
                * self._psi_spatial[(n_q, l_q, m_q)]
                * np.exp(-1j * energy_n(n_q) * t)
            )
        return psi

    def _recompute_surface(self):
        psi = self._psi_grid(self.time)
        rho = (psi * psi.conjugate()).real
        self.verts, self.faces = compute_isosurface(
            rho, self.coords, self.einschluss
        )

    def _has_beating(self):
        """True wenn Superposition verschiedene n hat -> |Psi|^2 aendert sich."""
        return len({s[0] for s in self.states}) > 1

    # == Rendering ====================================
    def _redraw(self):
        self.ax3d.cla()
        self._style_ax(self.ax3d)

        if self.verts is None or self.faces is None:
            self.ax3d.text2D(
                0.5, 0.5, "Keine Fl\u00e4che gefunden",
                transform=self.ax3d.transAxes,
                color="red", ha="center", fontsize=12,
            )
            self.fig.canvas.draw_idle()
            return

        tri = self.verts[self.faces]
        centroids = tri.mean(axis=1)

        if self.show_phase:
            psi_c = psi_at_points(self.states, centroids, self.time)
            colors = phase_to_rgba(psi_c, alpha=0.7)
        else:
            z = centroids[:, 2]
            zmin, zmax = z.min(), z.max()
            if zmax - zmin < 1e-12:
                zmax = zmin + 1
            colors = plt.cm.coolwarm((z - zmin) / (zmax - zmin))

        mesh = Poly3DCollection(tri, alpha=0.7, edgecolor="none", linewidths=0)
        mesh.set_facecolor(colors)
        self.ax3d.add_collection3d(mesh)

        e = self.extent
        self.ax3d.set_xlim(-e, e)
        self.ax3d.set_ylim(-e, e)
        self.ax3d.set_zlim(-e, e)

        pct = int(self.einschluss * 100)
        lbl = ", ".join(f"|{s[0]},{s[1]},{s[2]}\u27e9" for s in self.states)
        mode = "Phase" if self.show_phase else "|\u03a8|\u00b2"
        self.ax3d.set_title(
            f"{lbl}  |  {pct}%  |  {mode}  |  t = {self.time:.1f}",
            color="white", fontsize=10, pad=8,
        )
        self.fig.canvas.draw_idle()

    # == Animation ====================================
    def _start_anim(self):
        if self.anim is not None:
            return
        beating = self._has_beating()

        def step(_frame):
            self.time += self.dt
            if beating:
                self._recompute_surface()
            self._redraw()
            return []

        self.anim = animation.FuncAnimation(
            self.fig, step, interval=80, blit=False, cache_frame_data=False
        )
        self.fig.canvas.draw_idle()

    def _stop_anim(self):
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None

    # == Styling ======================================
    @staticmethod
    def _style_ax(ax):
        ax.set_facecolor("#0f0f1a")
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor("#333")
        ax.yaxis.pane.set_edgecolor("#333")
        ax.zaxis.pane.set_edgecolor("#333")
        ax.tick_params(colors="gray", labelsize=7)
        ax.set_xlabel("X", color="gray", labelpad=4)
        ax.set_ylabel("Y", color="gray", labelpad=4)
        ax.set_zlabel("Z", color="gray", labelpad=4)
        ax.grid(True, color="#222", linewidth=0.4)


# =============================================
if __name__ == "__main__":
    Simulation()
