import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.gridspec import GridSpec
from scipy.special import sph_harm_y, genlaguerre

# ─────────────────────────────────────────────
#  Wahrscheinlichkeitsfelder
# ─────────────────────────────────────────────

n = 1
l = 0
m = 0
a0 = 1

def hydrogen_eigenstate(n, l, m, r, theta, phi):
    Sqrt = np.sqrt((2 / (n * a0))**3 * math.factorial(n - l - 1) / (2 * n * math.factorial(n + l)))
    laguerre = genlaguerre(n - l - 1, 2 * l + 1)(2 * r / (n * a0))
    sperical_harmonic = sph_harm_y(m, l, phi, theta)
    Psi = Sqrt * np.exp(-r / (n * a0)) * (2 * r / (n * a0))**l * laguerre * sperical_harmonic
    
    return Psi


def eigenstates(X, Y, Z):
    r = np.sqrt(X**2 + Y**2 + Z**2)
    r_safe = np.where(r == 0, 1e-30, r)  # Division durch Null vermeiden
    Theta = np.arccos(np.clip(Z / r_safe, -1, 1))
    Phi = np.arctan2(Y, X)
    
    Psi = hydrogen_eigenstate(n, l, m, r, Theta, Phi)
    return np.abs(Psi)**2  # reelle Wahrscheinlichkeitsdichte

FELDER = {
    "Hydrogen Eigenstates": eigenstates,
}


# ─────────────────────────────────────────────
#  Sampling-Kern
# ─────────────────────────────────────────────

def gewichtetes_grid_sampling(
    feld_func,
    n_punkte: int = 3000,
    aufloesung: int = 40,
    bereich: tuple = (-5.0, 5.0),
) -> np.ndarray:
    """
    Erstellt ein diskretes 3D-Gitter, berechnet das Wahrscheinlichkeitsfeld
    und zieht n_punkte gewichtet aus den Gitterpunkten.

    Returns: Array (n_punkte, 3) mit x, y, z Koordinaten + kleinem Jitter
    """
    lo, hi = bereich
    coords = np.linspace(lo, hi, aufloesung)
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")

    # Feld berechnen und normieren
    gewichte = np.real(feld_func(X, Y, Z)).astype(float).ravel()
    gewichte = np.nan_to_num(gewichte, nan=0.0)      # NaN → 0
    gewichte = np.clip(gewichte, 0, None)             # keine negativen Werte
    gewichte /= gewichte.sum()                        # → Wahrscheinlichkeiten

    # Indizes gewichtet ziehen
    idx = np.random.choice(len(gewichte), size=n_punkte, p=gewichte)

    # Gitterpunkte + zufälliger Jitter (halbe Gitterschrittweite)
    schrittweite = (hi - lo) / (aufloesung - 1)
    jitter = np.random.uniform(-schrittweite / 2, schrittweite / 2,
                               size=(n_punkte, 3))

    punkte = np.column_stack([
        X.ravel()[idx],
        Y.ravel()[idx],
        Z.ravel()[idx],
    ]) + jitter

    return punkte


# ─────────────────────────────────────────────
#  Visualisierung
# ─────────────────────────────────────────────

class Simulation:
    def __init__(self):
        self.feld_name  = "Hydrogen Eigenstates"
        self.n_punkte   = 2000
        self.aufloesung = 35
        self.farb_achse = "Z"
        self.punkte     = None

        self._build_gui()
        self._update()
        plt.show()

    # ── GUI aufbauen ───────────────────────────
    def _build_gui(self):
        self.fig = plt.figure(figsize=(14, 9), facecolor="#1a1a2e")
        self.fig.suptitle(
            "3D-Punktsimulation · Gewichtetes Grid-Sampling",
            color="white", fontsize=14, fontweight="bold", y=0.98
        )

        gs = GridSpec(
            3, 3,
            figure=self.fig,
            left=0.01, right=0.72,
            top=0.93, bottom=0.05,
            wspace=0.05, hspace=0.05,
        )

        # Haupt-3D-Plot
        self.ax3d = self.fig.add_subplot(gs[:, :2], projection="3d")
        self._style_ax(self.ax3d)

        # ── Steuerelemente rechts ──────────────
        ctrl_left = 0.65

        # Feldauswahl (RadioButtons)
        ax_radio = self.fig.add_axes([ctrl_left, 0.60, 0.22, 0.32],
                                     facecolor="#0f0f1a")
        ax_radio.set_title("Wahrscheinlichkeitsfeld",
                            color="white", fontsize=9, pad=6)
        self.radio = RadioButtons(
            ax_radio, list(FELDER.keys()),
            activecolor="#e94560"
        )
        for lbl in self.radio.labels:
            lbl.set_color("white")
            lbl.set_fontsize(8)
        self.radio.on_clicked(self._on_feld)

        # Slider: Anzahl Punkte
        ax_sl_n = self.fig.add_axes([ctrl_left, 0.47, 0.22, 0.04],
                                    facecolor="#0f0f1a")
        self.sl_n = Slider(ax_sl_n, "Punkte", 200, 8000,
                           valinit=self.n_punkte, valstep=100,
                           color="#e94560")
        self.sl_n.label.set_color("white")
        self.sl_n.valtext.set_color("white")
        self.sl_n.on_changed(self._on_slider)

        # Slider: Auflösung
        ax_sl_r = self.fig.add_axes([ctrl_left, 0.38, 0.22, 0.04],
                                    facecolor="#0f0f1a")
        self.sl_r = Slider(ax_sl_r, "Auflösung", 10, 60,
                           valinit=self.aufloesung, valstep=5,
                           color="#0f3460")
        self.sl_r.label.set_color("white")
        self.sl_r.valtext.set_color("white")
        self.sl_r.on_changed(self._on_slider)

        # RadioButtons: Farbachse
        ax_farbe = self.fig.add_axes([ctrl_left, 0.22, 0.22, 0.13],
                                     facecolor="#0f0f1a")
        ax_farbe.set_title("Farbe nach Achse", color="white",
                            fontsize=9, pad=6)
        self.radio_farbe = RadioButtons(
            ax_farbe, ["X", "Y", "Z", "Dichte"],
            activecolor="#e94560"
        )
        for lbl in self.radio_farbe.labels:
            lbl.set_color("white")
            lbl.set_fontsize(8)
        self.radio_farbe.on_clicked(self._on_farbe)

        # Button: Neu berechnen
        ax_btn = self.fig.add_axes([ctrl_left, 0.10, 0.22, 0.07],
                                   facecolor="#0f0f1a")
        self.btn = Button(ax_btn, "▶  Neu sampeln",
                          color="#e94560", hovercolor="#c73652")
        self.btn.label.set_color("white")
        self.btn.label.set_fontsize(10)
        self.btn.on_clicked(self._on_btn)

    # ── Eventhandler ──────────────────────────
    def _on_feld(self, label):
        self.feld_name = label
        self._update()

    def _on_slider(self, _):
        self.n_punkte   = int(self.sl_n.val)
        self.aufloesung = int(self.sl_r.val)

    def _on_farbe(self, label):
        self.farb_achse = label
        self._redraw()

    def _on_btn(self, _):
        self.n_punkte   = int(self.sl_n.val)
        self.aufloesung = int(self.sl_r.val)
        self._update()

    # ── Kern-Update ───────────────────────────
    def _update(self):
        self.punkte = gewichtetes_grid_sampling(
            FELDER[self.feld_name],
            n_punkte=self.n_punkte,
            aufloesung=self.aufloesung,
        )
        self._redraw()

    def _redraw(self):
        pts = self.punkte
        farben = self._farbwerte(pts)

        # ── 3D-Plot ──
        self.ax3d.cla()
        self._style_ax(self.ax3d)
        sc = self.ax3d.scatter(
            pts[:, 0], pts[:, 1], pts[:, 2],
            c=farben, cmap="plasma",
            s=4, alpha=0.6, linewidths=0,
        )
        self.ax3d.set_title(
            f"{self.feld_name}  |  {len(pts):,} Punkte",
            color="white", fontsize=10, pad=8
        )

        self.fig.canvas.draw_idle()

    # ── Hilfsmethoden ─────────────────────────
    def _farbwerte(self, pts):
        mapping = {"X": pts[:, 0], "Y": pts[:, 1], "Z": pts[:, 2]}
        if self.farb_achse in mapping:
            return mapping[self.farb_achse]
        # Dichte: Abstand zum nächsten Zentrum der Punktwolke
        center = pts.mean(axis=0)
        return -np.linalg.norm(pts - center, axis=1)

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


# ─────────────────────────────────────────────
if __name__ == "__main__":
    Simulation()