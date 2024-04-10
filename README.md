# DAVIS Weather Station - API
A Davis weather station was installed for RWTH Aachen University's EmBaLu research project on emission-based ventilation control in road tunnels. The aim of the research project is to reduce the operating costs of the Einhorn Tunnel in Schwäbisch Gmünd by measuring pollutants in situ and regulating the tunnel ventilation accordingly. The meteorological data is used as the basis for dispersion calculations at the tunnel portals and the exhaust air stack. This API was created for automated retrieval of the measured data. 

#DAVIS_API.py
General API functions to request data from https://api.weatherlink.com for DAVIS weather stations. Including fuctions to get informations about the active stations, the last measurements and historic data.

#DAVIS_API.everyDay.py 
Recalls all measurements from the last 24 hours and appends them to a .csv file.
