(define (domain turing-machine-multi-action)
  (:requirements :strips :typing :negative-preconditions :conditional-effects :equality)
  (:types state symbol cell direction phase)
  
  (:predicates
    (currentState ?s - state)
    (headAt ?c - cell)
    (symbolAt ?c - cell ?sym - symbol)
    (transition ?z1 - state ?x - symbol ?z2 - state ?y - symbol ?d - direction)
    (adjacent ?d - direction ?c1 - cell ?c2 - cell)
    (haltingState ?s - state)
    (halted)
    
    ;; New predicates for execution phases
    (executionPhase ?p - phase)
    (nextPhase ?p1 ?p2 - phase)
    (readSymbol ?sym - symbol)     ;; Remember the symbol that was read
    (pendingState ?s - state)      ;; Remember the next state to transition to
    (pendingSymbol ?sym - symbol)  ;; Remember the symbol to write
    (pendingDirection ?d - direction) ;; Remember the direction to move
  )

  (:action read
    :parameters (?s - state ?c - cell ?sym - symbol ?p1 ?p2 - phase)
    :precondition (and
      (currentState ?s)
      (headAt ?c)
      (symbolAt ?c ?sym)
      (executionPhase ?p1)
      (nextPhase ?p1 ?p2)
      (not (haltingState ?s))
    )
    :effect (and
      (readSymbol ?sym)
      (not (executionPhase ?p1))
      (executionPhase ?p2)
    )
  )

  (:action decide-transition
    :parameters (?z1 - state ?x - symbol ?z2 - state ?y - symbol ?d - direction ?p1 ?p2 - phase)
    :precondition (and
      (currentState ?z1)
      (readSymbol ?x)
      (transition ?z1 ?x ?z2 ?y ?d)
      (executionPhase ?p1)
      (nextPhase ?p1 ?p2)
    )
    :effect (and
      (pendingState ?z2)
      (pendingSymbol ?y)
      (pendingDirection ?d)
      (not (executionPhase ?p1))
      (executionPhase ?p2)
    )
  )

  (:action write
    :parameters (?c - cell ?old-sym - symbol ?new-sym - symbol ?p1 ?p2 - phase)
    :precondition (and
      (headAt ?c)
      (symbolAt ?c ?old-sym)
      (pendingSymbol ?new-sym)
      (executionPhase ?p1)
      (nextPhase ?p1 ?p2)
    )
    :effect (and
      (not (symbolAt ?c ?old-sym))
      (symbolAt ?c ?new-sym)
      (not (executionPhase ?p1))
      (executionPhase ?p2)
    )
  )

  (:action change-state
    :parameters (?old-state - state ?new-state - state ?p1 ?p2 - phase)
    :precondition (and
      (currentState ?old-state)
      (pendingState ?new-state)
      (executionPhase ?p1)
      (nextPhase ?p1 ?p2)
    )
    :effect (and
      (when (not (= ?old-state ?new-state))
        (not (currentState ?old-state))
      )
      (currentState ?new-state)
      (not (executionPhase ?p1))
      (executionPhase ?p2)
    )
  )

  (:action move
    :parameters (?c1 - cell ?c2 - cell ?d - direction ?p1 ?p2 - phase)
    :precondition (and
      (headAt ?c1)
      (pendingDirection ?d)
      (adjacent ?d ?c1 ?c2)
      (executionPhase ?p1)
      (nextPhase ?p1 ?p2)
    )
    :effect (and
      (not (headAt ?c1))
      (headAt ?c2)
      (not (executionPhase ?p1))
      (executionPhase ?p2)
      (not (readSymbol ?sym)) ;; Clear the temporary predicates
      (not (pendingState ?s))
      (not (pendingSymbol ?sym))
      (not (pendingDirection ?d))
    )
  )

  (:action halt
    :parameters (?s - state)
    :precondition (and 
      (haltingState ?s) 
      (currentState ?s)
    )
    :effect (halted)
  )
)