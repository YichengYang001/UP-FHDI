#! /bin/bash

#Load the specific python compiler that has built-in GUI library
MODULE_PYTHON="python/3.6.5-fwk5uaj"

if module list 2>&1| grep -qw "$MODULE_PYTHON"; then
   echo "=======$MODULE_PYTHON was already loaded!========"
else
   module load python/3.6.5-fwk5uaj
   echo "=======$MODULE_PYTHON has been successfully loaded!========="
fi

#########################
if [ -d "test_env" ]
then 
   echo "========Virtual environment already exists!========="
   if [[ "$VIRTUAL_ENV" != "" ]]
   then
      echo "========VM mode already activated!========="
   else
      source test_env/bin/activate
      echo "=========VM mode successfully activated!======="
   fi
else
   python -m venv test_env # Create virtual environment
   source test_env/bin/activate # activate virtual environment
   pip install --upgrade pip # upgrade pip to the latest version
   pip install tinydb # install required packages
   echo "========New virtual environment with required packages is successfully created!========"
fi


#Load Intel compiler for UP-FHDI
MODULE_INTEL="intel/18.3"

if module list 2>&1| grep -qw "$MODULE_INTEL"; then
   echo "===========$MODULE_INTEL was already loaded!==========="
else
   module load intel/18.3
   echo "===========$MODULE_INTEL has been successfully loaded!==========="
fi

#Run GUI
python UP-FHDI.py #&

sleep 3 #avoid incorrect COMPLETE print, let bullet fly three second
echo "------ Job Status ----"
sacct -u $USER -n --format State | tail -1
echo -e "----------------------\n\n"

running_flag=1


while true
do
  #squeue -u $USER
  #echo $SLURM_JOB_ID
  #squeue -u $USER

  sleep 3 #avoid incorrect COMPLETE print, let bullet fly three second

#   echo "------ Job Status ----"
#   sacct -u $USER -n --format State | tail -1
#   echo -e "----------------------\n\n"

  #PENDING
  #RUNNING
  #COMPLETED
  if [ $(sacct -u $USER -n --format State | tail -1) == "COMPLETED" ]
  then
      echo "====================================================="
      echo "Job done! Please check output directory for results."
      echo "====================================================="
      break
  fi

  if [ $(sacct -u $USER -n --format State | tail -1) == "RUNNING" ]
  then
      echo "------ Job Status ----"
      echo "Your Submitted Job is Running"
      echo -e "----------------------\n\n"
  fi

  #echo $running_flag

done

