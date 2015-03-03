import numpy, numexpr

fast_eqn_map = {
    1 : (   '1.0 - 4.0 * c2 * (sqrt(c1) * (time - c0))',
            '((1.0 - sqrt(q)) / (2.0 * c2))**2'),

    2 : (   'sqrt(c1) * (time - c0)',
            '(q * (1.0 + c2 * q) * (1.0 + c3 * q * q))**2'),

    3 : (   '1.0 - 4.0 * c2 * (sqrt(c1 / c3) * (time - c0))',
            'c3 * ((1.0 - sqrt(q)) / (2.0 * c2))**2'),

    4 : (   '1.0 - 4.0 * c2 * (sqrt(c1 / c3) * (time - c0))',
            'c3 * ((1.0 - sqrt(q)) / (2.0 * c2)) **2 * (1.0 + c4 * (1.0 - ((1.0 - sqrt(q)) / (2.0 * c2)) ** 2) ** 3)')
}

time_solver = 'start_time + index * time_increment'

def solve_mass(start_time, time_increment, calibration, length):
    index = numpy.arange(length)
    time = numexpr.evaluate(time_solver)

    eqn = fast_eqn_map[calibration.equationType]
    c0, c1, c2, c3, c4 = calibration.constants[0:5]
    
    q = numexpr.evaluate(eqn[0])
    mass = numexpr.evaluate(eqn[1])

    return mass
