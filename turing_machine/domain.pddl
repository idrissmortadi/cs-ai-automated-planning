(define (domain turing-machine)
  (:requirements :strips :typing :negative-preconditions :conditional-effects :equality)
  (:types state symbol cell direction)
  (:predicates
    (currentState ?s - state)
    (headAt ?c - cell)
    (symbolAt ?c - cell ?sym - symbol)
    (transition ?z1 - state ?x - symbol ?z2 - state ?y - symbol ?d - direction)
    (adjacent ?d - direction ?c1 - cell ?c2 - cell)
    (haltingState ?s - state)
    (halted)
  )
  
   (:action step
    :parameters (?z1 - state ?x - symbol ?z2 - state ?y - symbol ?c1 - cell ?c2 - cell ?d - direction)
    :precondition (and
      (currentState ?z1)
      (headAt ?c1)
      (symbolAt ?c1 ?x)
      (transition ?z1 ?x ?z2 ?y ?d)
      (adjacent ?d ?c1 ?c2)
      )
    :effect (and
      (when (not (= ?z1 ?z2))
        (not (currentState ?z1))
      )
      (currentState ?z2)  ; Always set the current state to z2
      (not (symbolAt ?c1 ?x))
      (symbolAt ?c1 ?y)
      (not (headAt ?c1))
      (headAt ?c2)
    )
  ) 

  (:action halt
      :parameters (?s - state)
      :precondition (and (haltingState ?s) (currentState ?s))
      :effect (and (halted))
  )
  
)