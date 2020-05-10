        # contact 
        #   1) detected when the DC = DCdef
        #   2) detected during DC growth for estimated contactable time
        #   3) detected during DC growth for serendipitous contacts
        #   4) detected when the DC keeps low

        #   CP for sigma = n(2)/n(all detected contacts)
        #   CP for gamma = n(3)/n(all detected contacts)

Adaptive_Duty_Cycle = 0
init_duty_cycle = 0
sleep_duty_cycle = 0

AWAKE_ENERGY = 329.9
SLEEP_ENERGY = 4.02

first_case = 0
second_case = 0
third_case = 0
fourth_case = 0

second_case_rev = 0
third_case_rev = 0

_PRD = False    #dc temp > sleep dc?
_SRD = False    #extra dc


# while (current time != end time)
#------------if contact detection---------------


if (Adaptive_Duty_Cycle == init_duty_cycle):
    first_case += 1
elif (Adaptive_Duty_Cycle > init_duty_cycle):
    second_case += 1
elif (Adaptive_Duty_Cycle > sleep_duty_cycle and
    Adaptive_Duty_Cycle < init_duty_cycle):
    third_case += 1
elif (Adaptive_Duty_Cycle == sleep_duty_cycle):
    fourth_case += 1

if (_PRD):
    second_case_rev += 1
elif (_SRD):
    third_case_rev += 1


# Energy(k) = the amount of energy consumed in a day k
detected_contacts = first_case + second_case + third_case + fourth_case
CP_s = second_case/detected_contacts
CP_g = third_case/detected_contacts
#Energy = 

