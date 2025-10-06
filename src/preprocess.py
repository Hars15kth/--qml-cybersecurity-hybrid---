import os
import numpy as np
import pandas as pd

UNSW_COLS = [
    "srcip", "sport", "dstip", "dsport", "proto", "state", "dur", "sbytes", "dbytes", "sttl", "dttl", "sloss", "dloss",
    "service", "Sload", "Dload", "Spkts", "Dpkts", "swin", "dwin", "stcpb", "dtcpb", "smeansz", "dmeansz", "trans_depth",
    "res_bdy_len", "Sjit", "Djit", "Stime", "Ltime", "Sintpkt", "Dintpkt", "tcprtt", "synack", "ackdat",
    "ct_state_ttl", "ct_flw_http_mthd", "is_ftp_login", "ct_ftp_cmd", "ct_srv_src",
    "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm", "attack_cat", "label"
]
UNSW_COLS = [c.replace("ct_src_ ltm", "ct_src_ltm") for c in UNSW_COLS]

def load_unsw(parts, gt_path, feat_path, assume_no_headers=True):
    dfs = []
    for p in parts:
        dfp = pd.read_csv(p, low_memory=False, header=None if assume_no_headers else 'infer')
        if assume_no_headers or (len(dfp.columns) != len(UNSW_COLS)):
            dfp.columns = UNSW_COLS[:len(dfp.columns)]
        dfs.append(dfp)
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df.columns = [c.strip().lower() for c in df.columns]

    if gt_path and os.path.exists(gt_path):
        gt = pd.read_csv(gt_path, low_memory=False)
        gt.columns = [c.strip().lower() for c in gt.columns]
        keys = ["srcip", "sport", "dstip", "dsport", "proto", "stime"]
        try:
            df = df.merge(gt, on=keys, how="left", suffixes=("", "_gt"))
        except:
            pass

    if "label" not in df.columns:
        df["label"] = (df["attack_cat"].fillna("Normal").str.lower() != "normal").astype(int)
    if "attack_cat" not in df.columns:
        df["attack_cat"] = np.where(df["label"] == 1, "attack", "normal")

    numeric_cols = [
        "sport", "dsport", "dur", "sbytes", "dbytes", "sttl", "dttl", "sloss", "dloss",
        "swin", "dwin", "stcpb", "dtcpb", "smeansz", "dmeansz", "trans_depth",
        "ltime", "sintpkt", "dintpkt", "tcprtt", "synack", "ackdat"
    ]
    for col in numeric_cols:
        c = col.lower()
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["label"]).reset_index(drop=True)
    df["label"] = df["label"].astype(int)
    return df