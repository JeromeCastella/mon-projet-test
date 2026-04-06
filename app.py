import csv
import io
import base64
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)


def lire_ventes():
    totals = defaultdict(float)
    rows = []
    with open('data.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            totals[row['produit']] += float(row['montant'])
    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    grand_total = sum(totals.values())
    return rows, ranked, grand_total


def generer_graphique_base64(ranked):
    produits = [p for p, _ in ranked]
    montants = [m for _, m in ranked]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(produits, montants, color='steelblue')
    ax.set_title('Ventes par produit', fontsize=14, pad=12)
    ax.set_ylabel('Montant (CHF)')
    ax.tick_params(axis='x', rotation=10)
    for bar, val in zip(bars, montants):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 30,
                f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


@app.route('/')
def ventes():
    rows, ranked, grand_total = lire_ventes()
    graphique = generer_graphique_base64(ranked)
    return render_template('ventes.html',
                           rows=rows,
                           ranked=ranked,
                           grand_total=grand_total,
                           graphique=graphique)


if __name__ == '__main__':
    app.run(debug=True)
