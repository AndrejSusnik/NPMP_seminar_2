import numpy as np
import os

from hill_functions import *   
#from hill_functions import *   
 
"""
###
RELEVANT CODE FOR NPMP
###
"""
# MASTER-SLAVE D FLIP-FLOP MODEL
def ff_ode_model(Y, T, params): 
    
    a, not_a, q, not_q, d, clk = Y
    alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n = params

    da_dt     = alpha1*(pow(d/Kd, n)/(1 + pow(d/Kd, n) + pow(clk/Kd, n) + pow(d/Kd, n)*pow(clk/Kd, n))) + alpha2*(1/(1 + pow(not_a/Kd, n))) - delta1 *a 
    dnot_a_dt = alpha1*(1/(1 + pow(d/Kd, n) + pow(clk/Kd, n) + pow(d/Kd, n)*pow(clk/Kd, n))) + alpha2*(1/(1 + pow(a/Kd, n))) - delta1*not_a   
    dq_dt     = alpha3*((pow(a/Kd, n)*pow(clk/Kd, n))/(1 + pow(a/Kd, n) + pow(clk/Kd, n) + pow(a/Kd, n)*pow(clk/Kd, n))) + alpha4*(1/(1 + pow(not_q/Kd, n))) - delta2*q  
    dnot_q_dt = alpha3*((pow(not_a/Kd, n)*pow(clk/Kd, n))/(1 + pow(not_a/Kd, n) + pow(clk/Kd, n) + pow(not_a/Kd, n)*pow(clk/Kd, n))) + alpha4*(1/(1 + pow(q/Kd, n))) - delta2*not_q   


    return np.array([da_dt, dnot_a_dt, dq_dt, dnot_q_dt]) 

# XOR gate model


def xor(in1, in2, kd, n):
    return hybrid(in1, in2, kd, n, kd, n) + hybrid(in2, in1, kd, n, kd, n)

def xor1(in1, not_in1, in2, not_in2, kd, n):
    return activate_2(in1 + in2, not_in1 + not_in2, kd, n)
    return activate_2(in2, not_in1, kd, n) + activate_2(in1, not_in2, kd, n)

def four_bit_lfsr_34(Y, T, params_ff):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4, d1_in, d2_in, d3_in, d4_in, xor34 = Y

    clk = get_clock(T) 


    alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n = params_ff

    d1 = d1_in # xor34
    d2 = d2_in # q1
    d3 = d3_in # q2
    d4 = d4_in # q3

    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

    dY1 = ff_ode_model(Y_FF1, T, params_ff)
    dY2 = ff_ode_model(Y_FF2, T, params_ff)
    dY3 = ff_ode_model(Y_FF3, T, params_ff)
    dY4 = ff_ode_model(Y_FF4, T, params_ff)


    dY_xor34 = alpha1 * xor(q3, q4, Kd, n) - delta2 * xor34

    dY_d1_in = alpha1 * activate_1(xor34, Kd, n) - delta1 * d1_in
    dY_d2_in = alpha1 * activate_1(q1, Kd, n) - delta1 * d2_in
    dY_d3_in = alpha1 * activate_1(q2, Kd, n) - delta1 * d3_in
    dY_d4_in = alpha1 * activate_1(q3, Kd, n) - delta1 * d4_in

    output = [dY1, dY2, dY3, dY4, dY_d1_in, dY_d2_in, dY_d3_in, dY_d4_in, dY_xor34]

    dY = np.array([])
    for out in output:
        dY = np.append(dY, out)

    return dY

def eight_bit_lfsr(Y, T, params_ff):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4, a5, not_a5, q5, not_q5, a6, not_a6, q6, not_q6, a7, not_a7, q7, not_q7, a8, not_a8, q8, not_q8, d1_in, d2_in, d3_in, d4_in, d5_in, d6_in, d7_in, d8_in, xor82, xor83, xor84 = Y

    clk = get_clock(T) 

    alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n = params_ff

    d1 = d1_in # q8
    d2 = d2_in # q1
    d3 = d3_in # xor82
    d4 = d4_in # xor83
    d5 = d5_in # xor86
    d6 = d6_in # q5
    d7 = d7_in # q6
    d8 = d8_in # q7

    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]
    Y_FF5 = [a5, not_a5, q5, not_q5, d5, clk]
    Y_FF6 = [a6, not_a6, q6, not_q6, d6, clk]
    Y_FF7 = [a7, not_a7, q7, not_q7, d7, clk]
    Y_FF8 = [a8, not_a8, q8, not_q8, d8, clk]

    dY1 = ff_ode_model(Y_FF1, T, params_ff)
    dY2 = ff_ode_model(Y_FF2, T, params_ff)
    dY3 = ff_ode_model(Y_FF3, T, params_ff)
    dY4 = ff_ode_model(Y_FF4, T, params_ff)
    dY5 = ff_ode_model(Y_FF5, T, params_ff)
    dY6 = ff_ode_model(Y_FF6, T, params_ff)
    dY7 = ff_ode_model(Y_FF7, T, params_ff)
    dY8 = ff_ode_model(Y_FF8, T, params_ff)
    
    dY_xor82 = alpha1 * xor(q2, q8, Kd, n) - delta2 * xor82
    dY_xor83 = alpha1 * xor(q3, q8, Kd, n) - delta2 * xor83
    dY_xor84 = alpha1 * xor(q4, q8, Kd, n) - delta2 * xor84
    
    
    dY_d1_in = alpha1 * activate_1(q8, Kd, n) - delta1 * d1_in
    dY_d2_in = alpha1 * activate_1(q1, Kd, n) - delta1 * d2_in
    dY_d3_in = alpha1 * activate_1(xor82, Kd, n) - delta1 * d3_in
    dY_d4_in = alpha1 * activate_1(xor83, Kd, n) - delta1 * d4_in
    dY_d5_in = alpha1 * activate_1(xor84, Kd, n) - delta1 * d5_in
    dY_d6_in = alpha1 * activate_1(q5, Kd, n) - delta1 * d6_in
    dY_d7_in = alpha1 * activate_1(q6, Kd, n) - delta1 * d7_in
    dY_d8_in = alpha1 * activate_1(q7, Kd, n) - delta1 * d8_in
    
    output = [dY1, dY2, dY3, dY4, dY5, dY6, dY7, dY8, dY_d1_in, dY_d2_in, dY_d3_in, dY_d4_in, dY_d5_in, dY_d6_in, dY_d7_in, dY_d8_in, dY_xor82, dY_xor83, dY_xor84]

    dY = np.array([])
    for out in output:
        dY = np.append(dY, out)
    return dY
"""
JOHSON COUNTER MODELS 
"""
	
# TOP MODEL (JOHNSON): ONE BIT MODEL WITH EXTERNAL CLOCK
def one_bit_model(Y, T, params):
    a, not_a, q, not_q= Y

    clk = get_clock(T) 

    d = not_q
    Y_FF1 = [a, not_a, q, not_q, d, clk]

    dY = ff_ode_model(Y_FF1, T, params)

    return dY

# TOP MODEL (JOHNSON): TWO BIT MODEL WITH EXTERNAL CLOCK    
def two_bit_model(Y, T, params): 
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2 = Y

    clk = get_clock(T) 

    d1 = not_q2
    d2 = q1
    
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]

    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)

    dY = np.append(dY1, dY2)

    return dY

# TOP MODEL (JOHNSON): THREE BIT MODEL WITH EXTERNAL CLOCK    
def three_bit_model(Y, T, params):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3 = Y

    clk = get_clock(T) 

    d1 = not_q3
    d2 = q1
    d3 = q2
    
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]

    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)
    dY3 = ff_ode_model(Y_FF3, T, params)

    dY = np.append(np.append(dY1, dY2), dY3)

    return dY

# TOP MODEL (JOHNSON): FOUR BIT MODEL WITH EXTERNAL CLOCK    
def four_bit_model(Y, T, params):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y

    clk = get_clock(T) 

    d1 = not_q4
    d2 = q1
    d3 = q2
    d4 = q3

    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)
    dY3 = ff_ode_model(Y_FF3, T, params)
    dY4 = ff_ode_model(Y_FF4, T, params)

    dY = np.append(np.append(np.append(dY1, dY2), dY3), dY4)

    return dY


"""
###
END OF RELEVANT CODE FOR NPMP
###
"""


"""
JOHSON COUNTER MODELS THAT USE FLIP-FLOPS WITH ASYNCRHONOUS SET/RESET
dodano 23. 1. 2020
"""
	
# TOP MODEL (JOHNSON): ONE BIT MODEL WITH EXTERNAL CLOCK AND FLIP-FLOPS WITH ASYNCRHONOUS SET/RESET
def one_bit_model_RS(Y, T, params):
    a, not_a, q, not_q, R, S = Y

    clk = get_clock(T) 

    d = not_q
    Y_FF1 = [a, not_a, q, not_q, d, clk, R, S]

    dY = ff_ode_model_RS(Y_FF1, T, params)
    
    return dY

# TOP MODEL (JOHNSON): TWO BIT MODEL WITH EXTERNAL CLOCK AND FLIP-FLOPS WITH ASYNCRHONOUS SET/RESET    
def two_bit_model_RS(Y, T, params): 
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, R1, S1, R2, S2 = Y

    clk = get_clock(T) 

    d1 = not_q2
    d2 = q1
    
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk, R1, S1]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk, R2, S2]

    dY1 = ff_ode_model_RS(Y_FF1, T, params)
    dY2 = ff_ode_model_RS(Y_FF2, T, params)

    dY = np.append(dY1, dY2)

    return dY

# TOP MODEL (JOHNSON): THREE BIT MODEL WITH EXTERNAL CLOCK AND FLIP-FLOPS WITH ASYNCRHONOUS SET/RESET    
def three_bit_model_RS(Y, T, params):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, R1, S1, R2, S2, R3, S3 = Y

    clk = get_clock(T) 

    d1 = not_q3
    d2 = q1
    d3 = q2

       
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk, R1, S1]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk, R2, S2]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk, R3, S3]

    dY1 = ff_ode_model_RS(Y_FF1, T, params)
    dY2 = ff_ode_model_RS(Y_FF2, T, params)
    dY3 = ff_ode_model_RS(Y_FF3, T, params)

    dY = np.append(np.append(dY1, dY2), dY3)

    return dY




"""
###
OTHER CODE
###
"""


"""
FLIP-FLOP MODELS
"""
# MASTER-SLAVE D FLIP-FLOP QSSA MODEL
def ff_stochastic_model(Y, T, params, omega):
	p = np.zeros(12)  

	a, not_a, q, not_q, d, clk = Y
	alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n = params
    
	p[0] = alpha1*(pow(d/(Kd*omega), n)/(1 + pow(d/(Kd*omega), n) + pow(clk/(Kd*omega), n) + pow(d/(Kd*omega), n)*pow(clk/(Kd*omega), n)))*omega   
	p[1] = alpha2*(1/(1 + pow(not_a/(Kd*omega), n)))*omega    
	p[2] = delta1*a  
	p[3] = alpha1*(1/(1 + pow(d/(Kd*omega), n) + pow(clk/(Kd*omega), n) + pow(d/(Kd*omega), n)*pow(clk/(Kd*omega), n)))*omega   
	p[4] = alpha2*(1/(1 + pow(a/(Kd*omega), n)))*omega   
	p[5] = delta1*not_a 
	p[6] = alpha3*((pow(a/(Kd*omega), n)*pow(clk/(Kd*omega), n))/(1 + pow(a/(Kd*omega), n) + pow(clk/(Kd*omega), n) + pow(a/(Kd*omega), n)*pow(clk/(Kd*omega), n)))*omega
	p[7] = alpha4*(1/(1 + pow(not_q/(Kd*omega), n)))*omega   
	p[8] = delta2*q 
	p[9] = alpha3*((pow(not_a/(Kd*omega), n)*pow(clk/(Kd*omega), n))/(1 + pow(not_a/(Kd*omega), n) + pow(clk/(Kd*omega), n) + pow(not_a/(Kd*omega), n)*pow(clk/(Kd*omega), n)))*omega   
	p[10] = alpha4*(1/(1 + pow(q/(Kd*omega), n)))*omega 
	p[11] = delta2*not_q 

	#propensities     
	return p   
	
	

# FF MODEL WITH ASYNCHRONOUS RESET AND SET
# dodana parametra deltaE, KM
# dodani vhodni spremenljivki RESET in SET
# dodano 23. 1. 2020
def ff_ode_model_RS(Y, T, params): 
    
    a, not_a, q, not_q, d, clk, RESET, SET = Y

    repress_both = True

    if repress_both:
            sum_one = a + q
            sum_zero = not_a + not_q
    
    alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n, deltaE, KM = params


    da_dt     = alpha1*(pow(d/Kd, n)/(1 + pow(d/Kd, n) + pow(clk/Kd, n) + pow(d/Kd, n)*pow(clk/Kd, n))) + alpha2*(1/(1 + pow(not_a/Kd, n))) - delta1 *a 

    #deltaE = delta1
    if repress_both:
        da_dt += -a*(deltaE*RESET/(KM+sum_one))
    else:
        da_dt += -a*(deltaE*RESET/(KM+a))


    dnot_a_dt = alpha1*(1/(1 + pow(d/Kd, n) + pow(clk/Kd, n) + pow(d/Kd, n)*pow(clk/Kd, n))) + alpha2*(1/(1 + pow(a/Kd, n))) - delta1*not_a
    if repress_both:
        dnot_a_dt += -not_a*(deltaE*SET/(KM+sum_zero))
    else:
        dnot_a_dt += -not_a*(deltaE*SET/(KM+not_a))    


    #deltaE = delta2
    dq_dt     = alpha3*((pow(a/Kd, n)*pow(clk/Kd, n))/(1 + pow(a/Kd, n) + pow(clk/Kd, n) + pow(a/Kd, n)*pow(clk/Kd, n))) + alpha4*(1/(1 + pow(not_q/Kd, n))) - delta2*q
    if repress_both:
        dq_dt += -q*(deltaE*RESET/(KM+sum_one))
    
    dnot_q_dt = alpha3*((pow(not_a/Kd, n)*pow(clk/Kd, n))/(1 + pow(not_a/Kd, n) + pow(clk/Kd, n) + pow(not_a/Kd, n)*pow(clk/Kd, n))) + alpha4*(1/(1 + pow(q/Kd, n))) - delta2*not_q   
    if repress_both:
        dnot_q_dt += -not_q*(deltaE*SET/(KM+sum_zero))
   
    return np.array([da_dt, dnot_a_dt, dq_dt, dnot_q_dt]) 


"""
ADRESSING MODELS
"""

# ADDRESSING 1-BIT QSSA MODEL
def addressing_stochastic_one_bit_model(Y, T, params, omega):   
    alpha, delta, Kd, n = params
    _,_, q1, not_q1, i1, i2 = Y  
    p = np.zeros(4) 
	
    p[0] = alpha*activate_1(not_q1, Kd*omega, n)*omega  
    p[1] = delta*i1  
    p[2] = alpha*activate_1(q1, Kd*omega, n)*omega 
    p[3] = delta*i2
	
    #propensities    
    return p

# ADDRESSING 2-BIT QSSA MODEL 
def addressing_stochastic_two_bit_model(Y, T, params, omega):   
    alpha, delta, Kd, n = params
    _, _, q1, not_q1, _, _, q2, not_q2, i1, i2, i3, i4 = Y
    p = np.zeros(8)  
	
    p[0] = alpha * activate_2(not_q1, not_q2, Kd*omega, n)*omega 
    p[1] = delta * i1
    p[2] = alpha * activate_2(q1, not_q2, Kd*omega, n)*omega  
    p[3] = delta * i2 
    p[4] = alpha * activate_2(q1, q2, Kd*omega, n)*omega    
    p[5] = delta * i3  
    p[6] = alpha * activate_2(not_q1, q2, Kd*omega, n)*omega
    p[7] = delta * i4    
			
    #propensities    
    return p 

# ADDRESSING 3-BIT QSSA MODEL 
def addressing_stochastic_three_bit_model(Y, T, params, omega):   
    alpha, delta, Kd, n = params
    _, _, q1, not_q1, _, _, q2, not_q2, _, _, q3, not_q3, i1, i2, i3, i4, i5, i6 = Y 
    p = np.zeros(12)  
	
    p[0] = alpha * activate_2(not_q1, not_q3, Kd*omega, n)*omega
    p[1] = delta * i1
    p[2] = alpha * activate_2(q1, not_q2, Kd*omega, n)*omega 
    p[3] = delta * i2
    p[4] = alpha * activate_2(q2, not_q3, Kd*omega, n)*omega
    p[5] = delta * i3
    p[6] = alpha * activate_2(q1, q3, Kd*omega, n)*omega
    p[7] = delta * i4
    p[8] = alpha * activate_2(not_q1, q2, Kd*omega, n)*omega
    p[9] = delta * i5  
    p[10] = alpha * activate_2(not_q2, q3, Kd*omega, n)*omega  
    p[11] = delta * i6    	
	
	#propensities      
    return p   	 	

# ONE BIT ADDRESSING MODEL SIMPLE
def one_bit_simple_addressing_ode_model(Y, T, params):
    alpha, delta, Kd, n = params
    
    q1, not_q1, i1, i2 = Y

    di1_dt = alpha * activate_1(not_q1, Kd, n) - delta * i1
    di2_dt = alpha * activate_1(q1, Kd, n) - delta * i2
    
    return np.array([di1_dt, di2_dt])

   
# TWO BIT ADDRESSING MODEL SIMPLE
def two_bit_simple_addressing_ode_model(Y, T, params):
    alpha, delta, Kd, n = params
    
    q1, not_q1, q2, not_q2, i1, i2, i3, i4 = Y

    di1_dt = alpha * activate_2(not_q1, not_q2, Kd, n) - delta * i1
    di2_dt = alpha * activate_2(q1, not_q2, Kd, n) - delta * i2
    di3_dt = alpha * activate_2(q1, q2, Kd, n) - delta * i3
    di4_dt = alpha * activate_2(not_q1, q2, Kd, n) - delta * i4

    return np.array([di1_dt, di2_dt, di3_dt, di4_dt])

# THREE BIT ADDRESSING MODEL SIMPLE
def three_bit_simple_addressing_ode_model(Y, T, params):
    alpha, delta, Kd, n = params
    
    q1, not_q1, q2, not_q2, q3, not_q3, i1, i2, i3, i4, i5, i6 = Y

    di1_dt = alpha * activate_2(not_q1, not_q3, Kd, n) - delta * i1
    di2_dt = alpha * activate_2(q1, not_q2, Kd, n) - delta * i2
    di3_dt = alpha * activate_2(q2, not_q3, Kd, n) - delta * i3
    di4_dt = alpha * activate_2(q1, q3, Kd, n) - delta * i4
    di5_dt = alpha * activate_2(not_q1, q2, Kd, n) - delta * i5
    di6_dt = alpha * activate_2(not_q2, q3, Kd, n) - delta * i6

    return np.array([di1_dt, di2_dt, di3_dt, di4_dt, di5_dt, di6_dt])

# FOUR BIT ADDRESSING MODEL SIMPLE
def four_bit_simple_addressing_ode_model(Y, T, params):
    alpha, delta, Kd, n = params
    
    q1, not_q1, q2, not_q2, q3, not_q3, q4, not_q4, i1, i2, i3, i4, i5, i6, i7, i8 = Y

    di1_dt = alpha * activate_2(not_q1, not_q4, Kd, n) - delta * i1
    di2_dt = alpha * activate_2(q1, not_q2, Kd, n) - delta * i2
    di3_dt = alpha * activate_2(q2, not_q3, Kd, n) - delta * i3
    di4_dt = alpha * activate_2(q3, not_q4, Kd, n) - delta * i4
    
    di5_dt = alpha * activate_2(q1, q4, Kd, n) - delta * i5
    di6_dt = alpha * activate_2(not_q1, q2, Kd, n) - delta * i6
    di7_dt = alpha * activate_2(not_q2, q3, Kd, n) - delta * i7
    di8_dt = alpha * activate_2(not_q3, q4, Kd, n) - delta * i8


    return np.array([di1_dt, di2_dt, di3_dt, di4_dt, di5_dt, di6_dt, di7_dt, di8_dt])






"""
PROCESSOR MODEL


!!!OPTIMIZACIJA NAD TEMI MODELI!!!


"""

# TOP MODEL OF PROCESSOR WITH ONE BIT ADDRESSING
def one_bit_processor_ext(Y, T, params_johnson, params_addr):
    a1, not_a1, q1, not_q1, i1, i2  = Y

    Y_johnson = [a1, not_a1, q1, not_q1]
    Y_address = [q1, not_q1, i1, i2]
    
    
    dY_johnson = one_bit_model(Y_johnson, T, params_johnson)
    dY_addr = one_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY


# TOP MODEL OF PROCESSOR WITH TWO BIT ADDRESSING
def two_bit_processor_ext(Y, T, params_johnson, params_addr):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, i1, i2, i3, i4  = Y

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2]
    Y_address = [q1, not_q1, q2, not_q2, i1, i2, i3, i4]
    
    
    dY_johnson = two_bit_model(Y_johnson, T, params_johnson)
    dY_addr = two_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY

# TOP MODEL OF PROCESSOR WITH THREE BIT ADDRESSING
def three_bit_processor_ext(Y, T, params_johnson, params_addr):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, i1, i2, i3, i4, i5, i6  = Y

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3]
    Y_address = [q1, not_q1, q2, not_q2, q3, not_q3, i1, i2, i3, i4, i5, i6]
    
    
    dY_johnson = three_bit_model(Y_johnson, T, params_johnson)
    dY_addr = three_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY

# TOP MODEL OF PROCESSOR WITH FOUR BIT ADDRESSING
def four_bit_processor_ext(Y, T, params_johnson, params_addr):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4, i1, i2, i3, i4, i5, i6, i7, i8  = Y

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4]
    Y_address = [q1, not_q1, q2, not_q2, q3, not_q3, q4, not_q4, i1, i2, i3, i4, i5, i6, i7, i8]
    
    
    dY_johnson = four_bit_model(Y_johnson, T, params_johnson)
    dY_addr = four_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY



"""
PROCESSOR MODEL WITH EXTERNAL CLOCK AND RS inputs
external clock is required, more robust
jumps allowed
dodano 23. 1. 2020
"""

# TOP MODEL OF PROCESSOR WITH ONE BIT ADDRESSING AND FLIP-FLOP WITH RS ASYNCHRONOUS INPUTS
def one_bit_processor_ext_RS(Y, T, params_johnson_RS, params_addr):
    a1, not_a1, q1, not_q1, i1, i2  = Y

    R1 = 0
    S1 = 0

    Y_johnson = [a1, not_a1, q1, not_q1, R1, S1]
    Y_address = [q1, not_q1, i1, i2]
    
    
    dY_johnson = one_bit_model_RS(Y_johnson, T, params_johnson_RS)
    dY_addr = one_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY


# TOP MODEL OF PROCESSOR WITH TWO BIT ADDRESSING AND FLIP-FLOPS WITH RS ASYNCHRONOUS INPUTS
def two_bit_processor_ext_RS(Y, T, params_johnson_RS, params_addr):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, i1, i2, i3, i4  = Y

    R1 = 0
    S1 = 0
    R2 = 0
    S2 = 0

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, R1, S1, R2, S2]
    Y_address = [q1, not_q1, q2, not_q2, i1, i2, i3, i4]
    
    
    dY_johnson = two_bit_model_RS(Y_johnson, T, params_johnson_RS)
    dY_addr = two_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY

# TOP MODEL OF PROCESSOR WITH THREE BIT ADDRESSING AND FLIP-FLOPS WITH RS ASYNCHRONOUS INPUTS
def three_bit_processor_ext_RS(Y, T, params_johnson_RS, params_addr, jump_src, jump_dst, i_src, i_dst):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, i1, i2, i3, i4, i5, i6  = Y

    i_src = eval(i_src)
    
    R = [0,0,0]
    S = [0,0,0]

    for i in range(len(jump_src)):
        if jump_src[i] > jump_dst[i]:
                R[i] = i_src
        elif jump_src[i] < jump_dst[i]:
                S[i] = i_src

    R1, R2, R3 = R if T > 1 else [100,100,100]
    S1, S2, S3 = S

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, R1, S1, R2, S2, R3, S3]
    Y_address = [q1, not_q1, q2, not_q2, q3, not_q3, i1, i2, i3, i4, i5, i6]
    
    
    dY_johnson = three_bit_model_RS(Y_johnson, T, params_johnson_RS)
    dY_addr = three_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY

"""
PROCESSOR MODEL WITH EXTERNAL CLOCK AND RS inputs AND JUMP CONDITIONS
dodano 24. 1. 2020
"""
def get_condition(x0, delta, t):
        return x0 * np.e**(-delta*t)

# TOP MODEL OF PROCESSOR WITH THREE BIT ADDRESSING AND CONDITIONAL JUMPS
def three_bit_processor_ext_RS_cond(Y, T, params_johnson_RS, params_addr, jump_src, jump_dst, i_src, i_dst, condition):
    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, i1, i2, i3, i4, i5, i6  = Y

    x0_cond, delta_cond, KD_cond, condition_type = condition
    cond = get_condition(x0_cond, delta_cond, T)

    

    i_src = eval(i_src)   
    
    R = np.array([0,0,0])
    S = np.array([0,0,0])

    for i in range(len(jump_src)):
        if jump_src[i] > jump_dst[i]:
                R[i] = i_src
        elif jump_src[i] < jump_dst[i]:
                S[i] = i_src
    if condition_type == "induction":
        R = induction(R, cond, KD_cond)
        S = induction(S, cond, KD_cond)
    else:
        R = inhibition(R, cond, KD_cond)
        S = inhibition(S, cond, KD_cond)


    R1, R2, R3 = R
    S1, S2, S3 = S

    Y_johnson = [a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, R1, S1, R2, S2, R3, S3]
    Y_address = [q1, not_q1, q2, not_q2, q3, not_q3, i1, i2, i3, i4, i5, i6]
    
    
    dY_johnson = three_bit_model_RS(Y_johnson, T, params_johnson_RS)
    dY_addr = three_bit_simple_addressing_ode_model(Y_address, T, params_addr)

    dY = np.append(dY_johnson, dY_addr)
    return dY
