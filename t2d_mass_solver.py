from math import sqrt

def eqn_1(time, constants):
    c0, c1, c2 = constants[0:3]

    r1 = sqrt(c1) * (time - c0)
    q  = 1.0 - 4.0 * c2 * r1
    r2 = (1.0 - sqrt(q)) / (2.0 * c2)
    return r2**2

def eqn_2(time, constants):
    c0, c1, c2, c3 = constants[0:4]
    
    q = sqrt(c1) * (time - c0)
    r = q * (1.0 + c2 * q) * (1.0 + c3 * q * q)
    return r2**2

def eqn_3(time, constants):
    c0, c1, c2, c3 = constants[0:4]
    
    r1 = sqrt(c1 / c3) * (time - c0);
    q  = 1.0 - 4.0 * c2 * r1;
    r2 = (1.0 - sqrt(q)) / (2.0 * c2);
    return c3 * r2 * r2;

def eqn_4(time, constants):
    c0, c1, c2, c3, c4 = constants[0:5]
    
    r1 = sqrt(c1 / c3) * (time - c0);
    q  = 1.0 - 4.0 * c2 * r1;
    r2 = (1.0 - sqrt(q)) / (2.0 * c2);
    r3 = 1.0 - r2 * r2;
    return c3 * r2 * r2 * (1.0 + c4 * r3 * r3 * r3);

eqn_map = {
    1 : eqn_1,
    2 : eqn_2,
    3 : eqn_3,
    4 : eqn_4
}

def solve_mass(start_time, time_increment, index, calibration):
    eqn = eqn_map[calibration.equationType]
    time = time = start_time + index * time_increment
    return eqn(time, calibration.constants)