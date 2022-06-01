
class CSP():

    def __init__(self, cages, domains, neighbors, constraints):
        cages = cages or list(domains.keys())
        self.cages = cages
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.selectedDomains = None
        self.numberOfAssigns = 0

# ______________________________________________________________________________
# CSP Backtracking Search

def forwardCheckingAlgorithm(cspObject, varCage, domainOfCage, assigned, toBeRemoved):
    if cspObject.selectedDomains is None:
            cspObject.selectedDomains = {v: list(cspObject.domains[v]) for v in cspObject.cages}
    for B in cspObject.neighbors[varCage]:
        if B not in assigned:
            for b in cspObject.selectedDomains[B][:]:
                if not cspObject.constraints(varCage, domainOfCage, B, b):
                    cspObject.selectedDomains[B].remove(b)
                    if toBeRemoved is not None:
                        toBeRemoved.append((B, b))
            if not cspObject.selectedDomains[B]:
                return False
    return True


def ACAlgorithm(cspObject, cageVar, toBeRemoved):
    q = [(X, cageVar) for X in cspObject.neighbors[cageVar]]
    if q == None:
        q = [(Xi, Xk) for Xi in cspObject.cages for Xk in cspObject.neighbors[Xi]]
    if cspObject.selectedDomains == None:
            cspObject.selectedDomains = {v: list(cspObject.domains[v]) for v in cspObject.cages}
    while q:
        (Xi, Xj) = q.pop()
        revised = False
        for x in cspObject.selectedDomains[Xi][:]:
            if all(not cspObject.constraints(Xi, x, Xj, y) for y in cspObject.selectedDomains[Xj]):
                cspObject.selectedDomains[Xi].remove(x)
                if toBeRemoved is not None:
                    toBeRemoved.append((Xi, x))
                revised = True
       
        if revised:
            if not cspObject.selectedDomains[Xi]:
                return False
            for Xk in cspObject.neighbors[Xi]:
                if Xk != Xj:
                    q.append((Xk, Xi))
    return True

def backTrackingAlgorithm(cspObject,
                        inf='none'):

    def recursiveBacktrack(assigned):
        # print("assigned", assigned)
        # print("csp.cages", cspObject.cages)

        if  len(cspObject.cages)==len(assigned) :
            return assigned

        cageVar = first([unAssigned for unAssigned in cspObject.cages if unAssigned not in assigned])
        # print("cageVar", cageVar)
       
        for domainOfCage in (cspObject.selectedDomains or cspObject.domains)[cageVar]:
            # print("domainOfCage", domainOfCage)
            
            noOfConflicts = count((var in assigned and
                    not cspObject.constraints(cageVar, domainOfCage, var, assigned[var])) for var in cspObject.neighbors[cageVar])

            if 0 == noOfConflicts:
                assigned[cageVar] = domainOfCage
                cspObject.numberOfAssigns += 1

                if cspObject.selectedDomains is None:
                        cspObject.selectedDomains = {v: list(cspObject.domains[v]) for v in cspObject.cages}
                toBeRemoved = [(cageVar, a) for a in cspObject.selectedDomains[cageVar] if a != domainOfCage]
                cspObject.selectedDomains[cageVar] = [domainOfCage]

                if inf == 'none':
                    res = recursiveBacktrack(assigned)
                    if res is not None:
                        return res
                elif inf == 'forwad_checking':
                    if(forwardCheckingAlgorithm(cspObject, cageVar, domainOfCage, assigned, toBeRemoved)):
                        res = recursiveBacktrack(assigned)
                        if res is not None:
                            return res
                elif inf == 'ac3':
                    if(ACAlgorithm(cspObject, cageVar, toBeRemoved)):
                        res = recursiveBacktrack(assigned)
                        if res is not None:
                            return res 
                for B, b in toBeRemoved:
                    cspObject.selectedDomains[B].append(b)

        if cageVar in assigned:
            del assigned[cageVar]
        return None

    solve = recursiveBacktrack({})
    
    solveDictionary = dict(solve)
    firstCondition = len(solveDictionary) == len(cspObject.cages)

    secondCondition = all(count((var in solveDictionary and
                    not cspObject.constraints(variables, solveDictionary[variables], var, solveDictionary[var])) for var in cspObject.neighbors[variables]) == 0 for variables in cspObject.cages)


    check = firstCondition and secondCondition
    if check is False:
        solve = None
    return solve

def count(seq):
    return sum(bool(x) for x in seq)
def first(iterable):
    return iterable[0]
