(define (problem fibonacci)
  (:domain turing-machine)
  (:objects
    ;; States
    q0 q101 q102 q103 q104 q105 q106 q107 q108 q109
    q201 q202 q203 q204
    q301 q302 q303 q304 q305 q306 q307 q308 q309 q310 q311
    q401 q402 q403 q404
    q501 q502 q503
    q601 q602 q603 q604
    q701 q702 q703 q704
    q801 q802 q803 q804 q805 q806 q807 q808 q809
    qf - state

    ;; Symbols: b = blank, one = input, x and s are internal symbols.
    b one x s - symbol

    ;; Tape cells: assume 25 cells
    c1 c2 c3 c4 c5 c6 c7 c8 c9 c10
    c11 c12 c13 c14 c15 c16 c17 c18 c19 c20
    c21 c22 c23 c24 c25 - cell

    ;; Directions
    R L N - direction
  )
  (:init
    ;; Initial configuration: input n=2
    (currentState q0)
    (headAt c1)
    (symbolAt c1 one)
    (symbolAt c2 one)
    (symbolAt c3 b)
    (symbolAt c4 b)
    (symbolAt c5 b)
    (symbolAt c6 b)
    (symbolAt c7 b)
    (symbolAt c8 b)
    (symbolAt c9 b)
    (symbolAt c10 b)
    (symbolAt c11 b)
    (symbolAt c12 b)
    (symbolAt c13 b)
    (symbolAt c14 b)
    (symbolAt c15 b)
    (symbolAt c16 b)
    (symbolAt c17 b)
    (symbolAt c18 b)
    (symbolAt c19 b)
    (symbolAt c20 b)
    (symbolAt c21 b)
    (symbolAt c22 b)
    (symbolAt c23 b)
    (symbolAt c24 b)
    (symbolAt c25 b)

    ;; Transition definitions (rules 0 to 99)
    ;; Rule 0: q0,one -> q101, write x, move R
    (transition q0 one q101 x R)
    ;; Rule one: q101,one -> q101, write one, move R
    (transition q101 one q101 one R)
    ;; Rule 2: q101,b -> q102, write one, move R
    (transition q101 b q102 one R)
    ;; Rule 3: q102,b -> q103, write s, move R
    (transition q102 b q103 s R)
    ;; Rule 4: q103,b -> q104, write one, move R
    (transition q103 b q104 one R)
    ;; Rule 5: q104,b -> q601, write s, move L
    (transition q104 b q601 s L)
    ;; Rule 6: q105,b -> q106, write one, move L
    (transition q105 b q106 one L)
    ;; Rule 7: q106,s -> q701, write s, move L
    (transition q106 s q701 s L)
    ;; Rule 8: q107,s -> q108, write s, move L
    (transition q107 s q108 s L)
    ;; Rule 9: q107,one -> q107, write one, move L
    (transition q107 one q107 one L)
    ;; Rule 10: q108,s -> q109, write s, move N
    (transition q108 s q109 s N)
    ;; Rule 11: q108,one -> q108, write one, move L
    (transition q108 one q108 one L)
    ;; Rule 12: q109,s -> q109, write s, move R
    (transition q109 s q109 s R)
    ;; Rule 13: q109,one -> q109, write one, move R
    (transition q109 one q109 one R)
    ;; Rule 14: q109,b -> q201, write s, move N
    (transition q109 b q201 s N)
    ;; Rule 15: q201,s -> q202, write s, move L
    (transition q201 s q202 s L)
    ;; Rule 16: q201,one -> q201, write one, move L
    (transition q201 one q201 one L)
    ;; Rule 17: q202,s -> q203, write s, move R
    (transition q202 s q203 s R)
    ;; Rule 18: q202,one -> q202, write one, move L
    (transition q202 one q202 one L)
    ;; Rule 19: q202,b -> q203, write b, move R
    (transition q202 b q203 b R)
    ;; Rule 20: q203,s -> q301, write s, move N
    (transition q203 s q301 s N)
    ;; Rule 21: q203,one -> q204, write b, move R
    (transition q203 one q204 b R)
    ;; Rule 22: q204,s -> q204, write s, move R
    (transition q204 s q204 s R)
    ;; Rule 23: q204,one -> q204, write one, move R
    (transition q204 one q204 one R)
    ;; Rule 24: q204,b -> q201, write one, move L
    (transition q204 b q201 one L)
    ;; Rule 25: q301,s -> q302, write s, move L
    (transition q301 s q302 s L)
    ;; Rule 26: q302,s -> q303, write s, move L
    (transition q302 s q303 s L)
    ;; Rule 27: q302,b -> q302, write b, move L
    (transition q302 b q302 b L)
    ;; Rule 28: q303,s -> q304, write s, move R
    (transition q303 s q304 s R)
    ;; Rule 29: q303,one -> q303, write one, move L
    (transition q303 one q303 one L)
    ;; Rule 30: q303,b -> q304, write b, move R
    (transition q303 b q304 b R)
    ;; Rule 31: q304,s -> q308, write b, move N
    (transition q304 s q308 b N)
    ;; Rule 32: q304,one -> q305, write b, move R
    (transition q304 one q305 b R)
    ;; Rule 33: q305,s -> q306, write s, move R
    (transition q305 s q306 s R)
    ;; Rule 34: q305,one -> q305, write one, move R
    (transition q305 one q305 one R)
    ;; Rule 35: q306,s -> q307, write s, move L
    (transition q306 s q307 s L)
    ;; Rule 36: q306,one -> q307, write one, move L
    (transition q306 one q307 one L)
    ;; Rule 37: q306,b -> q306, write b, move R
    (transition q306 b q306 b R)
    ;; Rule 38: q307,b -> q302, write one, move L
    (transition q307 b q302 one L)
    ;; Rule 39: q308,one -> q309, write one, move L
    (transition q308 one q309 one L)
    ;; Rule 40: q308,b -> q308, write b, move R
    (transition q308 b q308 b R)
    ;; Rule 41: q309,b -> q310, write s, move L
    (transition q309 b q310 s L)
    ;; Rule 42: q310,s -> q311, write s, move R
    (transition q310 s q311 s R)
    ;; Rule 43: q310,b -> q310, write one, move L
    (transition q310 b q310 one L)
    ;; Rule 44: q311,s -> q501, write s, move R
    (transition q311 s q501 s R)
    ;; Rule 45: q311,one -> q311, write one, move R
    (transition q311 one q311 one R)
    ;; Rule 46: q401,s -> q402, write s, move L
    (transition q401 s q402 s L)
    ;; Rule 47: q401,one -> q401, write one, move L
    (transition q401 one q401 one L)
    ;; Rule 48: q402,s -> q403, write s, move L
    (transition q402 s q403 s L)
    ;; Rule 49: q402,one -> q402, write one, move L
    (transition q402 one q402 one L)
    ;; Rule 50: q403,s -> q403, write s, move L
    (transition q403 s q403 s L)
    ;; Rule 51: q403,one -> q404, write s, move L
    (transition q403 one q404 s L)
    ;; Rule 52: q404,s -> q404, write s, move R
    (transition q404 s q404 s R)
    ;; Rule 53: q404,one -> q404, write one, move R
    (transition q404 one q404 one R)
    ;; Rule 54: q404,b -> q201, write s, move N
    (transition q404 b q201 s N)
    ;; Rule 55: q404,x -> q801, write x, move N
    (transition q404 x q801 x N)
    ;; Rule 56: q501,s -> q502, write one, move N
    (transition q501 s q502 one N)
    ;; Rule 57: q501,one -> q501, write one, move R
    (transition q501 one q501 one R)
    ;; Rule 58: q502,one -> q502, write one, move R
    (transition q502 one q502 one R)
    ;; Rule 59: q502,b -> q503, write b, move L
    (transition q502 b q503 b L)
    ;; Rule 60: q503,one -> q401, write b, move L
    (transition q503 one q401 b L)
    ;; Rule 61: q601,s -> q602, write s, move L
    (transition q601 s q602 s L)
    ;; Rule 62: q601,one -> q601, write one, move L
    (transition q601 one q601 one L)
    ;; Rule 63: q602,one -> q603, write s, move L
    (transition q602 one q603 s L)
    ;; Rule 64: q603,one -> q604, write one, move R
    (transition q603 one q604 one R)
    ;; Rule 65: q603,x -> q801, write x, move N
    (transition q603 x q801 x N)
    ;; Rule 66: q604,s -> q604, write s, move R
    (transition q604 s q604 s R)
    ;; Rule 67: q604,one -> q604, write one, move R
    (transition q604 one q604 one R)
    ;; Rule 68: q604,b -> q105, write b, move N
    (transition q604 b q105 b N)
    ;; Rule 69: q701,s -> q702, write s, move L
    (transition q701 s q702 s L)
    ;; Rule 70: q701,one -> q701, write one, move L
    (transition q701 one q701 one L)
    ;; Rule 71: q702,s -> q702, write s, move L
    (transition q702 s q702 s L)
    ;; Rule 72: q702,one -> q703, write s, move L
    (transition q702 one q703 s L)
    ;; Rule 73: q703,one -> q704, write one, move R
    (transition q703 one q704 one R)
    ;; Rule 74: q703,x -> q801, write x, move N
    (transition q703 x q801 x N)
    ;; Rule 75: q704,s -> q704, write s, move R
    (transition q704 s q704 s R)
    ;; Rule 76: q704,one -> q704, write one, move R
    (transition q704 one q704 one R)
    ;; Rule 77: q704,b -> q107, write b, move L
    (transition q704 b q107 b L)
    ;; Rule 78: q801,s -> q801, write s, move R
    (transition q801 s q801 s R)
    ;; Rule 79: q801,one -> q801, write one, move R
    (transition q801 one q801 one R)
    ;; Rule 80: q801,b -> q802, write b, move L
    (transition q801 b q802 b L)
    ;; Rule 81: q801,x -> q801, write x, move R
    (transition q801 x q801 x R)
    ;; Rule 82: q802,s -> q808, write b, move L
    (transition q802 s q808 b L)
    ;; Rule 83: q802,one -> q808, write one, move L
    (transition q802 one q808 one L)
    ;; Rule 84: q803,s -> q803, write s, move L
    (transition q803 s q803 s L)
    ;; Rule 85: q803,one -> q803, write s, move L
    (transition q803 one q803 s L)
    ;; Rule 86: q803,x -> q804, write x, move R
    (transition q803 x q804 x R)
    ;; Rule 87: q804,s -> q804, write s, move R
    (transition q804 s q804 s R)
    ;; Rule 88: q804,one -> q805, write s, move L
    (transition q804 one q805 s L)
    ;; Rule 89: q804,b -> q809, write b, move N
    (transition q804 b q809 b N)
    ;; Rule 90: q805,s -> q805, write s, move L
    (transition q805 s q805 s L)
    ;; Rule 91: q805,one -> q806, write one, move R
    (transition q805 one q806 one R)
    ;; Rule 92: q805,x -> q806, write s, move N
    (transition q805 x q806 s N)
    ;; Rule 93: q806,s -> q807, write one, move R
    (transition q806 s q807 one R)
    ;; Rule 94: q807,s -> q804, write s, move R
    (transition q807 s q804 s R)
    ;; Rule 95: q808,s -> q803, write s, move L
    (transition q808 s q803 s L)
    ;; Rule 96: q808,one -> q808, write one, move L
    (transition q808 one q808 one L)
    ;; Rule 97: q809,s -> q809, write b, move L
    (transition q809 s q809 b L)
    ;; Rule 98: q809,one -> qf, write one, move N
    (transition q809 one qf one N)
    ;; Rule 99: q809,b -> q809, write b, move L
    (transition q809 b q809 b L)

    ;; Adjacent cell definitions for cells c1 to c25.
    ;; Right-direction
    (adjacent R c1 c2)
    (adjacent R c2 c3)
    (adjacent R c3 c4)
    (adjacent R c4 c5)
    (adjacent R c5 c6)
    (adjacent R c6 c7)
    (adjacent R c7 c8)
    (adjacent R c8 c9)
    (adjacent R c9 c10)
    (adjacent R c10 c11)
    (adjacent R c11 c12)
    (adjacent R c12 c13)
    (adjacent R c13 c14)
    (adjacent R c14 c15)
    (adjacent R c15 c16)
    (adjacent R c16 c17)
    (adjacent R c17 c18)
    (adjacent R c18 c19)
    (adjacent R c19 c20)
    (adjacent R c20 c21)
    (adjacent R c21 c22)
    (adjacent R c22 c23)
    (adjacent R c23 c24)
    (adjacent R c24 c25)
    ;; Left-direction (inverse of right)
    (adjacent L c2 c1)
    (adjacent L c3 c2)
    (adjacent L c4 c3)
    (adjacent L c5 c4)
    (adjacent L c6 c5)
    (adjacent L c7 c6)
    (adjacent L c8 c7)
    (adjacent L c9 c8)
    (adjacent L c10 c9)
    (adjacent L c11 c10)
    (adjacent L c12 c11)
    (adjacent L c13 c12)
    (adjacent L c14 c13)
    (adjacent L c15 c14)
    (adjacent L c16 c15)
    (adjacent L c17 c16)
    (adjacent L c18 c17)
    (adjacent L c19 c18)
    (adjacent L c20 c19)
    (adjacent L c21 c20)
    (adjacent L c22 c21)
    (adjacent L c23 c22)
    (adjacent L c24 c23)
    (adjacent L c25 c24)

    ; N-direction (no movement)
    (adjacent N c1 c1)
    (adjacent N c2 c2)
    (adjacent N c3 c3)
    (adjacent N c4 c4)
    (adjacent N c5 c5)
    (adjacent N c6 c6)
    (adjacent N c7 c7)
    (adjacent N c8 c8)
    (adjacent N c9 c9)
    (adjacent N c10 c10)
    (adjacent N c11 c11)
    (adjacent N c12 c12)
    (adjacent N c13 c13)
    (adjacent N c14 c14)
    (adjacent N c15 c15)
    (adjacent N c16 c16)
    (adjacent N c17 c17)
    (adjacent N c18 c18)
    (adjacent N c19 c19)
    (adjacent N c20 c20)
    (adjacent N c21 c21)
    (adjacent N c22 c22)
    (adjacent N c23 c23)
    (adjacent N c24 c24)
    (adjacent N c25 c25)

    ;; Halting state
    (haltingState qf)
  )
  (:goal (halted))
)