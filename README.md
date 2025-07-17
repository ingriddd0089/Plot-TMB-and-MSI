# 📊 plot_group_tool

Reusable plotting utilities for analyzing and visualizing tumor mutational burden (TMB) and other features across clinical cohorts.

---

## 🧰 Features

- `get_TMB(df, capture_size)`: compute TMB per sample from a mutation matrix.
- `plot_distribution()`: generate clean histogram-style distribution plots.
- `plot_group_comparison()`: compare one or two cohorts using boxplots, with built-in statistical annotation.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 📂 Folder Structure

```
plot_group_tool/
├── plot_utils.py           # All plotting functions
├── requirements.txt        # Required Python packages
├── .gitignore              # Ignore notebooks, images, data
└── data/                   # <- Not uploaded, you must create this and put input files here
```

> 🔐 `.tiff`, `.png`, `.ipynb`, `data/` are all excluded from Git tracking.

---

## 📊 Example Usage

### Get TMB values:
```python
from plot_utils import get_TMB
get_TMB(mutation_df, capture_size=50000000)
```

### Plot distribution:
```python
plot_distribution(
    data=your_df,
    column='TMB',
    save_path='TMB_distribution'
)
```

### Plot group comparison:
```python
plot_group_comparison(
    df0=surgical_df,
    df1=non_surgical_df,
    column="TMB",
    ylabel="log(TMB)",
    title0="Surgical",
    title1="Non-surgical",
    group_column="status",
    group_order=["status 1", "status 2"],
    log_transform=True,
    save_path="TMB_comparison"
)
```

---

## 📄 License

This tool is intended for academic/non-commercial use. Contact the author for other applications.
