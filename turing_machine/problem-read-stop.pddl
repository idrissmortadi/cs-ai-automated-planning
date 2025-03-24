(define (problem tm-read-stop)
  (:domain turing-machine)
  (:objects
    z0 z1 qh - state
    blank one - symbol
    c0 c1 c2 - cell
    left right - direction
  )
  ; | c0 | c1 | c2 |
  ; |  1 |    |    |
  (:init
    (haltingState qh)
    (currentState z0)
    (headAt c0)

    (symbolAt c0 one)
    (symbolAt c1 blank)
    (symbolAt c2 blank)

    (adjacent left c1 c0)
    (adjacent left c2 c1)

    (adjacent right c0 c1)
    (adjacent right c1 c2)

    (transition z0 one z1 blank right)
    (transition z1 blank qh one left)
  )
  (:goal (halted))
)
