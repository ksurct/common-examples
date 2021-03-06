EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R1
U 1 1 6171FC85
P 4500 3450
F 0 "R1" H 4570 3496 50  0000 L CNN
F 1 "10K" H 4570 3405 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4430 3450 50  0001 C CNN
F 3 "~" H 4500 3450 50  0001 C CNN
	1    4500 3450
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 617206F4
P 5050 3450
F 0 "R2" H 5120 3496 50  0000 L CNN
F 1 "R" H 5120 3405 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4980 3450 50  0001 C CNN
F 3 "~" H 5050 3450 50  0001 C CNN
	1    5050 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 3300 5000 3300
Wire Wire Line
	4850 3300 4850 3050
Wire Wire Line
	4500 3050 4500 3300
Wire Wire Line
	4500 3050 4850 3050
Text GLabel 5050 3600 3    50   Input ~ 0
GND
Text GLabel 4500 3600 3    50   Input ~ 0
GND
$Comp
L temp_lib:arduino U1
U 1 1 61721D2F
P 5850 2900
F 0 "U1" H 5850 3425 50  0000 C CNN
F 1 "arduino" H 5850 3334 50  0000 C CNN
F 2 "temp_lib:arduino" H 5850 3300 50  0001 C CNN
F 3 "" H 5850 3300 50  0001 C CNN
	1    5850 2900
	1    0    0    -1  
$EndComp
$Comp
L temp_lib:arduino U3
U 1 1 61722814
P 6700 3250
F 0 "U3" H 6700 3775 50  0000 C CNN
F 1 "arduino" H 6700 3684 50  0000 C CNN
F 2 "temp_lib:arduino" H 6700 3650 50  0001 C CNN
F 3 "" H 6700 3650 50  0001 C CNN
	1    6700 3250
	1    0    0    -1  
$EndComp
$Comp
L temp_lib:arduino U2
U 1 1 61722C22
P 5900 4100
F 0 "U2" H 5900 4625 50  0000 C CNN
F 1 "arduino" H 5900 4534 50  0000 C CNN
F 2 "temp_lib:arduino" H 5900 4500 50  0001 C CNN
F 3 "" H 5900 4500 50  0001 C CNN
	1    5900 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 2600 6300 2600
Wire Wire Line
	6400 2600 6400 2950
Wire Wire Line
	6150 2800 6150 2950
Wire Wire Line
	6150 3100 6400 3100
Wire Wire Line
	6400 3100 6400 3050
Wire Wire Line
	6400 3150 6200 3150
Wire Wire Line
	6200 3150 6200 2700
Wire Wire Line
	6200 2700 6150 2700
Wire Wire Line
	6400 3250 6200 3250
Text GLabel 7000 2950 2    50   Input ~ 0
1
Text GLabel 7000 3050 2    50   Input ~ 0
4
Text GLabel 5600 3800 0    50   Input ~ 0
1
Text GLabel 5600 3900 0    50   Input ~ 0
4
Wire Wire Line
	6200 3900 6400 3900
Wire Wire Line
	6400 3900 6400 3650
Wire Wire Line
	6200 4000 5600 4000
Wire Wire Line
	5600 4100 5050 4100
Wire Wire Line
	5050 4100 5050 3600
Wire Wire Line
	5600 4200 4750 4200
Wire Wire Line
	4750 4200 4750 3300
Wire Wire Line
	4750 3300 4500 3300
Connection ~ 4500 3300
Wire Wire Line
	5550 2900 5000 2900
Wire Wire Line
	5000 2900 5000 3300
Connection ~ 5000 3300
Wire Wire Line
	5000 3300 4850 3300
Wire Wire Line
	5550 2800 5550 2900
Wire Wire Line
	5550 3350 6200 3350
Wire Wire Line
	6200 3250 6200 3350
Connection ~ 5550 2900
Wire Wire Line
	5550 2900 5550 3000
Connection ~ 5550 3000
Wire Wire Line
	5550 3000 5550 3350
Connection ~ 6200 3350
Wire Wire Line
	6200 3350 6200 3800
Wire Wire Line
	5550 2700 5450 2700
Wire Wire Line
	5450 2700 5450 2350
Wire Wire Line
	5450 2350 6300 2350
Wire Wire Line
	6300 2350 6300 2600
Connection ~ 6300 2600
Wire Wire Line
	6300 2600 6400 2600
Wire Wire Line
	5550 2600 5850 2600
Wire Wire Line
	5850 2600 5850 2950
Wire Wire Line
	5850 2950 6150 2950
Connection ~ 6150 2950
Wire Wire Line
	6150 2950 6150 3100
Wire Wire Line
	7000 3150 7000 3650
Wire Wire Line
	7000 3650 6400 3650
Connection ~ 6400 3650
Wire Wire Line
	6400 3650 6400 3350
$EndSCHEMATC
