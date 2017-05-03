import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_absolute_error
from camcan.datasets import load_camcan_connectivity_rest
import matplotlib.pyplot as plt

ATLAS = 'basc122'
METRIC = 'tangent'
CONN_DIR = '/storage/data/camcan_connectivity'
CSV_FILE = '/storage/data/cc700-scored/participant_data.csv'
dataset = load_camcan_connectivity_rest(
    data_dir=CONN_DIR, patients_info_csv=CSV_FILE,
    atlas=ATLAS, kind=METRIC)

X = np.array(dataset.connectivity)
y = np.array(dataset.scores['age'])
yr = np.ceil(y/10).astype(int)

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
r2s, maes = [], []
ytrue, ypred = [], []
svr = SVR(kernel='linear')

for iteration, (train, test) in enumerate(skf.split(X, yr)):
    svr.fit(X[train], y[train])
    yp = svr.predict(X[test])
    ytrue.extend(y[test])
    ypred.extend(yp)
    r2 = svr.score(X[test], y[test])
    mae = mean_absolute_error(y[test], yp)
    print('%u: R^2 %.2f - MAE %.2f' % (iteration, r2, mae))
    maes.append(mae)
    r2s.append(r2)

f = plt.figure(figsize=(6, 6))
ax = f.gca()
ax.scatter(ytrue, ypred)
ax.plot([0, 100], [0, 100], 'r', linewidth=2)
ax.grid(linestyle='--')
xlabels = ['%u' % x for x in ax.get_xticks()]
ax.set_xticklabels(xlabels, fontsize=26)
labels = ['%u' % x for x in ax.get_yticks()]
ax.set_yticklabels(labels, fontsize=26)
ax.set_ylabel('Predicted Age', fontsize=24)
ax.set_xlabel('True Age', fontsize=24)
ax.text(0, 90, 'r2=%.2f, mae=%.2f' % (np.mean(r2s), np.mean(maes)),
        fontsize=18)
ax.set_title('Connectivity-based prediction\n (svr, %s, %s)' % (ATLAS, METRIC),
             fontsize=20, fontweight='bold')
f.tight_layout()
f.savefig('/tmp/camcan_regression.png')
