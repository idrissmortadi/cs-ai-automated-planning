(define (problem tm-plus-one)
  (:domain turing-machine)
  (:objects
    z0 z1 zh - state
    sb s0 s1 - symbol
    c0 c1 c2 - cell
    L R C - direction
  )
  ; | c0 | c1 | c2 |
  ; |  1 |  0 |    |

  ; GOAL
  ; | c0 | c1 | c2 |
  ; |  1 |  1 |  0 |
  (:init
    (haltingState zh)
    (currentState z0)
    (headAt c0)

    (symbolAt c0 s1)
    (symbolAt c1 s0)
    (symbolAt c2 sb)

    (adjacent C c0 c0)
    (adjacent C c1 c1)
    (adjacent C c2 c2)

    ; For "move left" (decreasing cell index)
    (adjacent L c1 c0)  ; Moving left from c1 goes to c0
    (adjacent L c2 c1)  ; Moving left from c2 goes to c1
    
    ; For "move right" (increasing cell index)
    (adjacent R c0 c1)  ; Moving right from c0 goes to c1
    (adjacent R c1 c2)  ; Moving right from c1 goes to c2

    (transition z0 sb z1 sb L)
    (transition z1 sb zh s1 C)

    (transition z0 s0 z0 s0 R)
    (transition z1 s0 zh s1 C)
    
    (transition z0 s1 z0 s1 R)
    (transition z1 s1 z1 s0 L)
  )
  (:goal (halted))
)
