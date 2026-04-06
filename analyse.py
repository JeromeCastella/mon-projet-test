import csv
from collections import defaultdict

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
