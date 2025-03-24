;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Hanoi Tower Domain
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Header and description

(define (domain hanoi)
  (:requirements :strips :disjunctive-preconditions)
  
  (:predicates
    (on ?x ?y)      ; disk ?x is on disk or peg ?y
    (clear ?x)      ; disk or peg ?x has nothing on top of it
    (smaller ?x ?y) ; disk ?x is smaller than disk ?y
    (disk ?x)       ; ?x is a disk
    (peg ?x)        ; ?x is a peg
  )
  
  (:action move
    :parameters (?disk ?from ?to)
    :precondition (and
      (disk ?disk)
      (clear ?disk)
      (clear ?to)
      (on ?disk ?from)
      (or (peg ?to)
          (and (disk ?to) (smaller ?disk ?to)))
    )
    :effect (and
      (not (on ?disk ?from))
      (not (clear ?to))
      (on ?disk ?to)
      (clear ?from)
    )
  )
)