# **UP-FHDI GUI**

Graphical user interface for ultra data-oriented parallel fractional hot-deck imputation (UP-FHDI). UP-FHDI is a general-purpose, assumption-free imputation software capable of curing big missing data. 

- [Benchmarks](#Benchmarks)
- [Usage](#Usage)
  - [Dependencies](#Dependencies)
  - [Command](#Command)
- [Citation](#Citation)
- [Acknowledgements](#Acknowledgements)




Please see a tutorial video in [Tutorial for GUI](https://www.youtube.com/watch?v=7dZcUYYGyMw&t=331s) to illustrate the use of UP-FHDI software with example datasets.

# Benchmarks

| Dataset  | # Instances | # Variables | Missing rate | Header | Delimiter | Missing symbol | Source |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Synthetic.csv  | 100  | 80 | 30% | No | Comma | ? | Synthetic |
| Bias.txt  | 2100  | 23 | 30% | Yes | Tab |NA |UCI repository |

# Usage
## Dependencies

- [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
- [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
- Python>=3.6 with built-in Tkinter
- [TinyDB](https://github.com/msiemens/tinydb)
- Intel MPI

UP-FHDI software is recommended to be used on Windows since compatibility on Mac has not been broadly validated. Please see [X Forwarding for Mac and Windows](https://researchit.las.iastate.edu/guides/pronto/interactive_computing/x_forwarding/) to configure PuTTY to work with VcXsrv.
<br/><br/>
## Command
Run the following command on HPC for a quick deployment:
```python
source auto.sh
```

# Citation
Please kindly cite the following papers if you find this software useful. Thanks!
- Yicheng Yang and Qi Li, 2023. UP-FHDI: a software for big incomplete data curing, _ISU Digital Repository_.
- Yicheng Yang, Yonghyun Kwon, Jaekwang Kim, and In Ho Cho, 2022. Ultra data-oriented parallel fractional hot-deck imputation with efficient linearized variance estimation,  _IEEE Transactions on Knowledge and Data Engineering_ (revision invited).
- Yicheng Yang, Jaekwang Kim, and In Ho Cho, 2020. [Parallel fractional hot-deck imputation and variance estimation for big incomplete data curing](https://ieeexplore.ieee.org/document/9214981), _IEEE Transactions on Knowledge and Data Engineering_ 34(8), 3912-3926 [DOI: 10.1109/TKDE.2020.3029146].

```latex
@InProceedings{Yicheng:2023,
  author = {Yicheng Yang and Qi Li},
  title = {UP-FHDI: a software for big incomplete data curing},
  booktitle = {ISU Digital Repository},
  year = {2023},
}

@Article{Yicheng:2022, 
author = {Yicheng Yang and Yonghyun Kwon and Jaekwang Kim and In Ho Cho},
title = {Ultra data-oriented parallel fractional hot-deck
imputation with efficient linearized variance estimation},
journal = {IEEE Transactions on Knowledge and Data Engineering (revision invited)},
year = {2022},
}

@Article{Yicheng:2020,
  author = {Yicheng Yang and Jaekwang Kim and In Ho Cho},
  title = {Parallel fractional hot deck imputation and variance estimation for big incomplete data curing},
  journal = {IEEE Transactions on Knowledge and Data Engineering},
  year = {2020},
  volume = {34},
  number = {8},
  pages = {3912--3926},
  doi = {10.1109/TKDE.2020.3029146},
}
```

# Acknowledgements

This software is supported by National Science Foundation
(NSF) grant number OAC-1931380. The high-performance
computing facility used for this research is partially supported
by the HPC@ISU equipment at ISU, some of which have been
purchased through funding provided by NSF CNS 1229081
and CRI 1205413. Ultra data applications of this software used
the Extreme Science and Engineering Discovery Environment
(XSEDE), NSF ACI-1548562.
