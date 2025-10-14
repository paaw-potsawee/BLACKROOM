# OOD project

**Hilbert's hotel implementation in Python using B+ tree as data structure to store rooms**

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.7 or higher
- **pip** (Python package manager)
- _(Recommended)_ [virtualenv](https://virtualenv.pypa.io/) or [venv](https://docs.python.org/3/library/venv.html) for isolated Python environments

---

### Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/paaw-potsawee/BLACKROOM/
   cd BLACKROOM
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # Using venv (cross-platform)
   python -m venv .venv
   # On Unix/macOS
   source .venv/bin/activate
   # On Windows
   venv\Scripts\activate
   ```

3. **Install all dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

### Usage

**Run Black Room CLI**

```bash
python src/main.py
```

Enter initialize amount for room number : enter positive interger for number of guests in hotel

#### Commands

|  command  | description                               |
| :-------: | :---------------------------------------- |
|    `h`    | Help                                      |
|    `p`    | Print all guest data                      |
| `s <key>` | Search for a guest by key (room number)   |
| `r <key>` | Remove a guest by key (room number)       |
|    `i`    | Insert guest ([see below](#i-option))     |
|    `w`    | Write all guests data to file (hotel.csv) |
|    `q`    | Quit the program                          |

#### i option

| command | description                                       |
| :-----: | :------------------------------------------------ |
|   `m`   | Manual insert                                     |
|   `c`   | Select channel to insert ([see below](#c-option)) |

for option m

- enter number of to insert (if guest exists in that room will be replaced)

#### c option

| command | description                     |
| :-----: | :------------------------------ |
|   `1`   | walk in                         |
|   `2`   | Walk in (infinite guest number) |
|   `3`   | bus                             |
|   `4`   | bus (infinite bus)              |

- for each option enter number for guest(s) and bus(es) as needed

## Time Complexity Analysis (B+ Tree + Hotel flows)

This section documents precise, line-by-line cost model for B+ tree's core operation using T(n) = cn + d. Display in simple symbol

Constants

- N: total keys (rooms)
- m: order (max children per internal)
- b = m - 1: max pers node
- h $\approx \log_{\lceil m/2 \rceil} N$: approximate height of a B+ tree
- Key array type: array('Q') (unsigened 64-bit); per-comparison O(1).

### Big O of search, insert, delete will be added later

### Big O - Simple Standard Functions

| symbol         |          name          |
| -------------- | :--------------------: |
| $O(1),O(c)$    |     Constant time      |
| $O(log log n)$ |   Double logarithmic   |
| $O(log n)$     |       Logrithmic       |
| $O((log n)^2)$ |    Polylogarithmic     |
| $O(n)$         |         Linear         |
| $O(n log n)$   | Linearithmic/Loglinear |
| $O(n^2)$       |       Quadratic        |
| $O(n^c)$       |       Polynomial       |
| $O(c^n)$       |      Exponential       |
| $O(n!)$        |       Factorial        |
