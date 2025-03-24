(define (domain hamiltonian-cycle)
  (:requirements :strips :typing :equality :negative-preconditions)
  (:types vertex count)
  (:predicates
    (connected ?v1 ?v2 - vertex)       ; there is an edge between v1 and v2
    (visited ?v - vertex)              ; vertex v has been visited
    (current ?v - vertex)              ; current position in the path
    (start ?v - vertex)                ; starting vertex
    (path-length ?n - count)          ; number of vertices visited so far
    (next ?n1 ?n2 - count)            ; successor relation for counts
    (total-vertices ?n - count)       ; total number of vertices in the graph
  )
  
  (:action select-start
    :parameters (?v - vertex ?zero ?one - count)
    :precondition (and 
      (not (exists (?any - vertex) (start ?any)))  ; no start vertex selected yet
      (path-length ?zero)                          ; path length is zero
      (next ?zero ?one)                            ; one is the successor of zero
    )
    :effect (and
      (start ?v)                                   ; mark as start vertex
      (current ?v)                                 ; set as current position
      (visited ?v)                                 ; mark as visited
      (not (path-length ?zero))                    ; update path length
      (path-length ?one)                           ; path length is now one
    )
  )
  
  (:action move-to-next
    :parameters (?from ?to - vertex ?n1 ?n2 - count)
    :precondition (and
      (current ?from)                 ; we are at vertex "from"
      (connected ?from ?to)           ; there is an edge from "from" to "to"
      (not (visited ?to))             ; "to" hasn't been visited yet
      (path-length ?n1)               ; current path length
      (next ?n1 ?n2)                  ; n2 is successor of n1
    )
    :effect (and
      (not (current ?from))           ; no longer at "from"
      (current ?to)                   ; now at "to"
      (visited ?to)                   ; mark "to" as visited
      (not (path-length ?n1))         ; update path length
      (path-length ?n2)               ; increment path length
    )
  )
  
  (:action complete-cycle
    :parameters (?last ?first - vertex ?n - count)
    :precondition (and
      (current ?last)                 ; we are at vertex "last"
      (start ?first)                  ; "first" is the start vertex
      (connected ?last ?first)        ; there is an edge from "last" to "first"
      (path-length ?n)                ; current path length
      (total-vertices ?n)             ; all vertices have been visited
    )
    :effect (and
      (not (current ?last))           ; no longer at "last"
      (current ?first)                ; back at "first"
    )
  )
)