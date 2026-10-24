"""Create two GitHub-friendly SVG charts without third-party dependencies."""

import csv
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def read_rows(filename):
    with (ROOT / "results" / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def text(x, y, label, size=13, anchor="start", color="#203348", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'fill="{color}">{escape(str(label))}</text>')


def svg_document(width, height, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img">'
            '<rect width="100%" height="100%" fill="#ffffff"/>'
            + "".join(content) + '</svg>\n')


def comparison_chart():
    rows = read_rows("model_comparison.csv")
    parts = [text(36, 43, "AdaCon × AdaCon com Early Exit", 25, weight="bold"),
             text(36, 68, "COCO AP e GMAC por imagem — validação", 14, color="#617386")]
    panels = [("COCO AP (maior é melhor)", "ap_baseline", "ap_early_exit", 0.30, 120),
              ("GMAC (menor é melhor)", "gmac_baseline", "gmac_early_exit", 32.0, 560)]

    for title, base_key, early_key, maximum, x0 in panels:
        parts.append(text(x0, 117, title, 17, weight="bold"))
        for index, row in enumerate(rows):
            y = 164 + 95 * index
            parts.append(text(x0, y + 8, f'{row["branches"]}B', 15, weight="bold"))
            for offset, key, color, label in [(17, base_key, "#687f98", "Base"),
                                              (46, early_key, "#007f77", "Early Exit")]:
                value = float(row[key])
                bar_width = 260 * value / maximum
                parts.append(f'<rect x="{x0+36}" y="{y+offset}" width="{bar_width:.1f}" '
                             f'height="19" rx="3" fill="{color}"/>')
                display = f"{value:.4f}" if maximum < 1 else f"{value:.3f}"
                parts.append(text(x0 + 42 + bar_width, y + offset + 15, display, 12))
        parts.append(text(x0 + 36, 493, "Base", 13, color="#687f98"))
        parts.append(text(x0 + 106, 493, "Early Exit", 13, color="#007f77"))
    parts.append(text(36, 532, "Fonte: apresentação final do estudo (SIAC/UFRJ, 2026).", 12, color="#617386"))
    return svg_document(1000, 552, parts)


def tradeoff_chart():
    rows = read_rows("threshold_calibration.csv")
    parts = [text(35, 44, "Calibração do limiar de saída", 25, weight="bold"),
             text(35, 70, "AdaCon 2B · camada 58 · média ponderada", 14, color="#617386")]
    x_left, x_right, y_top, y_bottom = 100, 800, 120, 410
    for index in range(6):
        x = x_left + index * (x_right - x_left) / 5
        parts.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_bottom}" stroke="#e9edf1"/>')
        parts.append(text(x, 440, rows[index]["threshold"], 13, anchor="middle"))
    for value in (0, 20, 40, 60, 80, 100):
        y = y_bottom - (value / 100) * (y_bottom - y_top)
        parts.append(f'<line x1="{x_left}" y1="{y}" x2="{x_right}" y2="{y}" stroke="#e9edf1"/>')
        parts.append(text(x_left - 14, y + 4, f"{value}%", 12, anchor="end"))

    def points(column):
        return [(x_left + index * (x_right - x_left) / 5,
                 y_bottom - float(row[column]) / 100 * (y_bottom - y_top))
                for index, row in enumerate(rows)]

    for column, color, legend in [("ap_retained_pct", "#183c71", "AP preservado"),
                                  ("early_exit_pct", "#007f77", "Saídas antecipadas")]:
        coords = points(column)
        polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
        parts.append(f'<polyline points="{polyline}" stroke="{color}" stroke-width="3" fill="none"/>')
        for x, y in coords:
            parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        parts.append(text(450 if column == "ap_retained_pct" else 610, 493, legend, 14, color=color))
    parts.append(text(450, 462, "Limiar (τ)", 13, anchor="middle"))
    parts.append(text(35, 543, "Fonte: calibração reportada nos slides; valores diferentes dos da validação final.", 12, color="#617386"))
    return svg_document(910, 564, parts)


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    files = {"model_comparison.svg": comparison_chart(),
             "threshold_tradeoff.svg": tradeoff_chart()}
    for filename, content in files.items():
        target = FIGURES / filename
        target.write_text(content, encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
