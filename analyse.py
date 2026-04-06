import csv
from collections import defaultdict
import matplotlib.pyplot as plt

totals = defaultdict(float)

with open('data.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        totals[row['produit']] += float(row['montant'])

grand_total = sum(totals.values())
ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)

print("Total des ventes par produit")
print("-" * 46)
for produit, total in ranked:
    pct = total / grand_total * 100
    print(f"{produit:<28} {total:>8.2f} CHF  {pct:>5.1f}%")
print("-" * 46)
print(f"{'TOTAL':<28} {grand_total:>8.2f} CHF  100.0%")


def generer_graphique(totals, output='ventes.png'):
    produits = [p for p, _ in sorted(totals.items(), key=lambda x: x[1], reverse=True)]
    montants = [totals[p] for p in produits]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(produits, montants, color='steelblue')
    ax.set_title('Ventes par produit')
    ax.set_xlabel('Produit')
    ax.set_ylabel('Montant (CHF)')
    ax.tick_params(axis='x', rotation=15)
    fig.tight_layout()
    fig.savefig(output)
    print(f"Graphique sauvegardé : {output}")


generer_graphique(totals)
