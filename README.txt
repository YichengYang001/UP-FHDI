Graphical user interface for ultra data-oriented parallel fractional hot-deck imputation (UP-FHDI)
Developers: Yicheng Yang and Qi Li (Iowa State University)
Date released: Jan 1, 2023
References:
Y. Yang and Q. Li, "UP-FHDI: a software for big incomplete data curing," Theses and Dissertations, 2023.
Y. Yang, J. K. Kim, and I. H. Cho, "Ultra data-oriented parallel fractional hot-deck imputation with efficient linearized variance estimation," IEEE Transactions on Knowledge and Data Engineering (revision invited), 2022.



----------Dependencies-----------------
* VcXsrv
* PuTTY
* Python 3.6+ with built-in Tkinter
* TinyDB
* Intel MPI

 Please refer to reference papers for installing and configuring required dependencies. We recommend using UP-FHDI on Windows since compatibility on Mac has not been broadly validated.



-----------------------------------Example incomplete datasets---------------------------------------
 Note: incomplete data is represented by U(number of instances, number of variables, missing rate)

Synthetic incomplete dataset U(100,80,0.3): Synthetic.csv
Incomplete bias correction of numerical prediction model temperature forecast dataset from UCI repository U(2100,23,0.3): Bias.txt



--------------------Quick start-----------------
(1) Git clone this project to HPC storage.
(2) Upload the incomplete data to HPC storage.
(3) Run the shell script for a quick deployment:
    $ source auto.sh