import sys
from omniORB import CORBA, PortableServer
import CosNaming
import school__POA

class Etudiant:
    def __init__(self, matricule, nom, sexe, promotion, dateNaissance):
        self.matricule = matricule
        self.nom = nom
        self.sexe = sexe
        self.promotion = promotion
        self.dateNaissance = dateNaissance

class GestionEtudiantsImpl(school__POA.GestionEtudiants):
    def __init__(self):
        self.etudiants = {}

    def enregistrerEtudiant(self, e):
        self.etudiants[e.matricule] = e

    def modifierEtudiant(self, matricule, promotion, dateNaissance):
        if matricule in self.etudiants:
            self.etudiants[matricule].promotion = promotion
            self.etudiants[matricule].dateNaissance = dateNaissance

    def lireEtudiantsParPromotion(self, promotion):
        result = []
        for etudiant in self.etudiants.values():
            if etudiant.promotion == promotion:
                result.append(etudiant)
        return result

def main(argv):
    orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
    poa = orb.resolve_initial_references("RootPOA")
    poaManager = poa._get_the_POAManager()

    servant = GestionEtudiantsImpl()
    oid = poa.activate_object(servant)
    obj = servant._this()

    naming_context = orb.resolve_initial_references("NameService")
    root_context = naming_context._narrow(CosNaming.NamingContext)

    if root_context is None:
        print("Failed to narrow the root naming context")
        sys.exit(1)

    name = [CosNaming.NameComponent("GestionEtudiants", "")]
    try:
        root_context.bind(name, obj)
    except CosNaming.NamingContext.AlreadyBound:
        root_context.rebind(name, obj)

    poaManager.activate()
    print("Server is running...")
    orb.run()

if __name__ == "__main__":
    main(sys.argv)
