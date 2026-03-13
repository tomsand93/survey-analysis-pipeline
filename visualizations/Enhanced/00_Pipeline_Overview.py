#!/usr/bin/env python3
"""
Pipeline Overview Diagram - Enhanced two-row infographic.

Row 1: Five colour-coded pipeline steps with labels and descriptions.
Row 2: Data-file flow connecting every step.

Output: 00_Pipeline_Overview.png  (same directory as this script)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#f8fafc"
TEXT_DARK = "#0f172a"
TEXT_MID  = "#475569"
TEXT_LITE  = "#94a3b8"
ARROW_CLR = "#94a3b8"

STEPS = [
    {
        "num":      "01",
        "label":    "Discover",
        "icon_top": "LLM",
        "icon_bot": "Sample",
        "detail":   "Sample responses\nLLM surfaces themes",
        "color":    "#3b82f6",
        "dark":     "#1d4ed8",
        "pale":     "#dbeafe",
        "file_out": "discovered_\ncategories.json",
    },
    {
        "num":      "02",
        "label":    "Refine",
        "icon_top": "Merge",
        "icon_bot": "& Dedup",
        "detail":   "Consolidate &\ndeduplicate themes",
        "color":    "#8b5cf6",
        "dark":     "#6d28d9",
        "pale":     "#ede9fe",
        "file_out": "refined_\ncategories.json",
    },
    {
        "num":      "03",
        "label":    "Categorize",
        "icon_top": "LLM",
        "icon_bot": "Label",
        "detail":   "Assign 1-3 labels\nper response via LLM",
        "color":    "#f59e0b",
        "dark":     "#b45309",
        "pale":     "#fef3c7",
        "file_out": "full_data_\ncategorized.xlsx",
    },
    {
        "num":      "04",
        "label":    "Analyze",
        "icon_top": "Cross",
        "icon_bot": "Tabs",
        "detail":   "Aggregate results\ndemographic cross-tabs",
        "color":    "#22c55e",
        "dark":     "#15803d",
        "pale":     "#dcfce7",
        "file_out": "MULTI_CATEGORY\n_ANALYSIS.xlsx",
    },
    {
        "num":      "05",
        "label":    "Polish",
        "icon_top": "Format",
        "icon_bot": "Excel",
        "detail":   "Format & clean\nExcel output",
        "color":    "#ec4899",
        "dark":     "#9d174d",
        "pale":     "#fce7f3",
        "file_out": "Final\nReport",
    },
]

N         = len(STEPS)
FIG_W     = 16
FIG_H     = 7.5
BOX_W     = 2.1
BOX_H     = 2.2
FILE_H    = 0.7
FILE_W    = 1.7
ROW1_Y    = 3.6
ROW2_Y    = 1.2
STEP_GAP  = (FIG_W - N * BOX_W) / (N + 1)

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=150)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)


def txt(x, y, s, size=9, color=TEXT_DARK, weight="normal",
        ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, multialignment="center", **kw)


# ── Title ────────────────────────────────────────────────────────────────────
txt(FIG_W / 2, FIG_H - 0.45,
    "Survey Analysis Pipeline",
    size=20, color=TEXT_DARK, weight="bold")
txt(FIG_W / 2, FIG_H - 0.95,
    "LLM-powered multi-label categorisation of open-ended survey responses",
    size=10.5, color=TEXT_MID)

# ── Input node — fixed width, anchored at left margin ────────────────────────
IN_W  = 0.75
IN_X  = 0.08
IN_CX = IN_X + IN_W / 2
IN_CY = ROW2_Y + FILE_H / 2

in_box = FancyBboxPatch(
    (IN_X, ROW2_Y), IN_W, FILE_H,
    boxstyle="round,pad=0.06",
    facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.8,
)
ax.add_patch(in_box)
txt(IN_CX, IN_CY + 0.12, "XLSX", size=8, color="#0369a1", weight="bold")
txt(IN_CX, IN_CY - 0.13, "full_data.xlsx", size=6, color="#0369a1")

# ── Step boxes + file-out boxes ───────────────────────────────────────────────
step_centers = []

for i, step in enumerate(STEPS):
    x0 = STEP_GAP * (i + 1) + BOX_W * i
    cx = x0 + BOX_W / 2
    step_centers.append(cx)

    # Step box
    box = FancyBboxPatch(
        (x0, ROW1_Y), BOX_W, BOX_H,
        boxstyle="round,pad=0.12",
        facecolor=step["pale"],
        edgecolor=step["color"],
        linewidth=2.2,
    )
    ax.add_patch(box)

    # Step number badge
    badge = FancyBboxPatch(
        (x0 + 0.08, ROW1_Y + BOX_H - 0.38), 0.46, 0.3,
        boxstyle="round,pad=0.04",
        facecolor=step["color"], edgecolor="none",
    )
    ax.add_patch(badge)
    txt(x0 + 0.31, ROW1_Y + BOX_H - 0.22,
        step["num"], size=8, color="white", weight="bold")

    # Icon text (two lines, centred in a coloured circle-ish area)
    circle = plt.Circle((cx, ROW1_Y + BOX_H - 0.62), 0.32,
                         color=step["color"], zorder=3)
    ax.add_patch(circle)
    txt(cx, ROW1_Y + BOX_H - 0.56, step["icon_top"],
        size=7.5, color="white", weight="bold", zorder=4)
    txt(cx, ROW1_Y + BOX_H - 0.72, step["icon_bot"],
        size=7.5, color="white", weight="bold", zorder=4)

    # Step label
    txt(cx, ROW1_Y + 0.85, step["label"],
        size=11, color=step["dark"], weight="bold")

    # Detail
    txt(cx, ROW1_Y + 0.35, step["detail"],
        size=7.5, color=TEXT_MID)

    # Vertical connector: step box -> file row
    ax.annotate(
        "", xy=(cx, ROW2_Y + FILE_H + 0.02),
        xytext=(cx, ROW1_Y - 0.08),
        arrowprops=dict(
            arrowstyle="->,head_width=0.25,head_length=0.18",
            color=step["color"], lw=1.4,
        ),
    )

    # File-out box
    fx0  = cx - FILE_W / 2
    fbox = FancyBboxPatch(
        (fx0, ROW2_Y), FILE_W, FILE_H,
        boxstyle="round,pad=0.07",
        facecolor="white",
        edgecolor=step["color"],
        linewidth=1.5,
    )
    ax.add_patch(fbox)
    txt(cx, ROW2_Y + FILE_H / 2 + 0.10, step["file_out"].split("\n")[0],
        size=7, color=step["dark"], weight="bold")
    if "\n" in step["file_out"]:
        txt(cx, ROW2_Y + FILE_H / 2 - 0.12, step["file_out"].split("\n")[1],
            size=7, color=step["dark"], weight="bold")

# ── Horizontal arrows between step boxes ─────────────────────────────────────
for i in range(N - 1):
    x_start = STEP_GAP * (i + 1) + BOX_W * (i + 1)
    x_end   = STEP_GAP * (i + 2) + BOX_W * (i + 1)
    mid_y   = ROW1_Y + BOX_H / 2
    ax.annotate(
        "", xy=(x_end - 0.04, mid_y),
        xytext=(x_start + 0.04, mid_y),
        arrowprops=dict(
            arrowstyle="->,head_width=0.3,head_length=0.22",
            color=ARROW_CLR, lw=1.8,
        ),
    )

# ── Arrow: input node -> step-1 file box ────────────────────────────────────
ax.annotate(
    "", xy=(step_centers[0] - FILE_W / 2 - 0.05, ROW2_Y + FILE_H / 2),
    xytext=(IN_X + IN_W + 0.05, ROW2_Y + FILE_H / 2),
    arrowprops=dict(
        arrowstyle="->,head_width=0.25,head_length=0.18",
        color="#0284c7", lw=1.4,
    ),
)

# ── Horizontal dashed arrows between file-out boxes ───────────────────────────
for i in range(N - 1):
    x_start = step_centers[i]     + FILE_W / 2
    x_end   = step_centers[i + 1] - FILE_W / 2
    mid_y   = ROW2_Y + FILE_H / 2
    ax.annotate(
        "", xy=(x_end - 0.04, mid_y),
        xytext=(x_start + 0.04, mid_y),
        arrowprops=dict(
            arrowstyle="->,head_width=0.22,head_length=0.15",
            color=ARROW_CLR, lw=1.2,
            linestyle="dashed",
        ),
    )

# ── Row labels ────────────────────────────────────────────────────────────────
txt(0.35, ROW1_Y + BOX_H / 2, "STEPS", size=7.5, color=TEXT_LITE,
    weight="bold", rotation=90)
txt(0.35, ROW2_Y + FILE_H / 2, "FILES", size=7.5, color=TEXT_LITE,
    weight="bold", rotation=90)

# ── Tech badges at the bottom ─────────────────────────────────────────────────
BADGES = [
    "Ollama + Llama 3.2",
    "Runs fully locally",
    "Multi-label output",
    "Demographic cross-tabs",
]
badge_w     = 2.5
badge_total = len(BADGES) * badge_w + (len(BADGES) - 1) * 0.15
bx = (FIG_W - badge_total) / 2
by = 0.18
for label in BADGES:
    b = FancyBboxPatch(
        (bx, by), badge_w, 0.5,
        boxstyle="round,pad=0.08",
        facecolor="#e2e8f0", edgecolor="#cbd5e1", linewidth=1,
    )
    ax.add_patch(b)
    txt(bx + badge_w / 2, by + 0.25, label, size=8, color=TEXT_DARK)
    bx += badge_w + 0.15

# ── Save ──────────────────────────────────────────────────────────────────────
out_dir  = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "00_Pipeline_Overview.png")
plt.tight_layout(pad=0.3)
plt.savefig(out_path, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
print(f"Saved: {out_path}")
plt.close()
