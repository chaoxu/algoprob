{-# LANGUAGE DuplicateRecordFields #-}
module ProblemData where

import Data.Map.Strict (Map)



-- Ignore this file for now

-- Another idea
-- Each problem associated with different decorations
-- Including, input parameter, output parameter, complexity parameter, algorithms etc
-- decoration has types. For each type, it is either inheritable, or uninhabitable. 



-- defining the schema in haskell, so one can check it using HsYAML

-- standard problem are problems with a single query
-- this make sure data structure problems can be handled
-- also this might group together different problems
type ID                = String 
type ProblemID         = ID
type QueryID           = ID
type AlgorithmID       = ID
type DataStructureID   = ID
type AtomID            = ID
data Type = InputAtom | OutputAtom | ComplexityAtom | NoneAtom deriving Show
-- Complexity type? Time, Space, Oracle OracleID?
data Atom = Atom     {id               :: AtomID
                     , atomtype        :: Type
                     , name            :: String
                     , description     :: String
                     } deriving (Show)

data Problem = Problem {id             :: ProblemID
                     , name            :: String                       -- title of the problem
                     , description     :: String                       -- description that cannot be described from input and output
                     , algorithms      :: [Algorithm]                  -- algorithms for the problem
                     , inherit         :: [ProblemID]                  -- inherit from problems above
                     , parameters      :: [Atom]                       -- parameters
                     , note            :: String                       -- more description
                     } deriving (Show)

data Algorithm = Algorithm {id         :: AlgorithmID                  -- id for the algorithm (why do we need this?)
                     , name            :: String                       -- title of the problem
                     , description     :: String                       -- this would include reference and other stuff
                     , complexity      :: [Complexity]                 -- complexities of the algorithm
                     , subroutine      :: [Subroutine]                 -- subroutines of the algorithm, shared by each query
                                                                       -- maybe can be auto inferred?
                     } deriving (Show)


data DSProblem = DSProblem {id             :: ProblemID
                     , name            :: String                       -- title of the problem
                     , description     :: String                       -- simple description of the problem
                     , queries         :: [Query]                      -- queries
                     , dataStructures  :: [DataStructure]              -- algorithms for the problem
                     , inherit         :: [ProblemID]                  -- inherit from problems above
                     , parameters      :: [Atom]                       -- parameter inherent to the problem (only useful for data structures)
                     , note            :: String                       -- more description
                     } deriving (Show)


data Query = Query { id                :: QueryID 
                     , name            :: String                       -- title of the problem
                     , description     :: String                       -- simple description of the problem
                     , parameters      :: [Atom]                       -- all parameters
                     , note            :: String                       -- more description
                     } deriving (Show)



data DataStructure = DataStructure {id         :: DataStructureID                  -- id for the algorithm (why do we need this?)
                     , name            :: String                       -- title of the problem
                     , description     :: String                       -- this would include reference and other stuff
                     , complexity      :: Map QueryID [Complexity]     -- complexities of the algorithm
                     , subroutine      :: [Subroutine]                 -- subroutines of the algorithm, shared by each query
                                                                       -- maybe can be auto inferred?
                     } deriving (Show)
data Subroutine  = Subroutine { id :: String                           -- a subroutine is just problem and query
                     ,  problem    :: ProblemID
                     ,  query      :: QueryID
                     } deriving (Show)

data Complexity = Complexity {name     :: String  
                     , description     :: String
                     , _expression      :: Expression                  -- for computation over complexity
                     } deriving (Show) 

--type Expression = String

data Expression = Expression {
                     function :: Function,
                     parameters :: [Expression]
                  } deriving (Show)

data Function = Call SubroutineCall | Product | Sum | Log | Exp | Other String | Identity deriving Show

-- What to do when not all parameter is used?
-- those parameters will be set to maximum!
-- also how to handle cycles in a sane way?
data SubroutineCall = SubroutineCall {subroutine :: Subroutine
                        , usage :: Map Atom Expression      -- what variable to be replaced by which expression
} deriving (Show)