import torch
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
import numpy as np

def run_epoch(loader, model, opt=None, crit=None):
    train = opt is not None
    model.train() if train else model.eval()
    tot_l, tot_c, tot = 0.0, 0, 0
    for xb, yb in loader:
        if train:
            opt.zero_grad()
        logits = model(xb)
        loss = crit(logits, yb)
        if train:
            loss.backward()
            opt.step()
        tot_l += loss.item() * yb.size(0)
        tot_c += (logits.argmax(1) == yb).sum().item()
        tot += yb.size(0)
    return tot_l / tot, tot_c / tot

def collect_probs_preds(model, dl):
    model.eval()
    probs, preds, labels = [], [], []
    with torch.no_grad():
        for xb, yb in dl:
            logits = model(xb)
            p = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
            yhat = logits.argmax(1).cpu().numpy()
            probs.extend(p.tolist())
            preds.extend(yhat.tolist())
            labels.extend(yb.cpu().numpy().tolist())
    return np.array(preds), np.array(probs), np.array(labels)

def tune_threshold(probs, labels):
    prec, rec, thr = precision_recall_curve(labels, probs)
    f1s = 2 * (prec * rec) / (prec + rec + 1e-12)
    best_idx = f1s.argmax()
    best_thr = thr[max(best_idx - 1, 0)] if best_idx < len(thr) else 0.5
    return best_thr, f1s[best_idx], prec[best_idx], rec[best_idx]