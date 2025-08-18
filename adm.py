import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class GestionAdministrative:
    def __init__(self, fichier_data: str = "data_administration.json"):
        self.fichier_data = fichier_data
        self.donnees = self.charger_donnees()
    
    def charger_donnees(self) -> List[Dict]:
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.fichier_data):
            with open(self.fichier_data, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def sauvegarder_donnees(self) -> bool:
        """Sauvegarde les données dans le fichier JSON"""
        try:
            with open(self.fichier_data, 'w', encoding='utf-8') as f:
                json.dump(self.donnees, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {str(e)}")
            return False

    def afficher_menu(self) -> None:
        """Affiche le menu principal"""
        print("\n" + "="*50)
        print(" SYSTÈME DE GESTION ADMINISTRATIVE ".center(50, '='))
        print("="*50)
        print("1. Ajouter un enregistrement")
        print("2. Lister tous les enregistrements")
        print("3. Rechercher un enregistrement")
        print("4. Modifier un enregistrement")
        print("5. Supprimer un enregistrement")
        print("6. Statistiques")
        print("0. Quitter")
        print("="*50)

    def ajouter_enregistrement(self) -> None:
        """Ajoute un nouvel enregistrement"""
        print("\n--- Ajout d'un nouvel enregistrement ---")
        
        enregistrement = {
            'id': self.generer_id(),
            'nom': input("Nom complet : ").strip(),
            'matricule': input("Matricule : ").strip(),
            'service': input("Service : ").strip(),
            'poste': input("Poste occupé : ").strip(),
            'date_embauche': input("Date d'embauche (JJ/MM/AAAA) : ").strip(),
            'salaire': float(input("Salaire : ")),
            'date_creation': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        self.donnees.append(enregistrement)
        if self.sauvegarder_donnees():
            print("\n✅ Enregistrement ajouté avec succès !")
        else:
            print("\n❌ Erreur lors de l'ajout")

    def generer_id(self) -> int:
        """Génère un ID unique"""
        return max([e['id'] for e in self.donnees], default=0) + 1

    def lister_enregistrements(self, liste: List[Dict] = None) -> None:
        """Liste les enregistrements"""
        data = liste if liste is not None else self.donnees
        print(f"\n--- Liste des enregistrements ({len(data)} trouvés) ---")
        
        if not data:
            print("Aucun enregistrement trouvé.")
            return
            
        for idx, enreg in enumerate(data, 1):
            print(f"\nEnregistrement #{idx}")
            print(f"ID : {enreg['id']}")
            print(f"Nom : {enreg['nom']}")
            print(f"Matricule : {enreg['matricule']}")
            print(f"Service : {enreg['service']}")
            print(f"Poste : {enreg['poste']}")
            print(f"Date embauche : {enreg['date_embauche']}")
            print(f"Salaire : {enreg['salaire']:.2f} €")
            print("-"*40)

    def rechercher_enregistrement(self) -> None:
        """Recherche des enregistrements"""
        terme = input("\nEntrez un terme de recherche (nom, matricule, service) : ").lower()
        if not terme:
            print("Veuillez entrer un terme de recherche.")
            return
            
        resultats = [
            e for e in self.donnees 
            if (terme in e['nom'].lower() or 
                terme in e['matricule'].lower() or 
                terme in e['service'].lower())
        ]
        
        self.lister_enregistrements(resultats)

    def modifier_enregistrement(self) -> None:
        """Modifie un enregistrement existant"""
        self.lister_enregistrements()
        if not self.donnees:
            return
            
        try:
            id_modif = int(input("\nEntrez l'ID de l'enregistrement à modifier : "))
            enreg = next((e for e in self.donnees if e['id'] == id_modif), None)
            
            if enreg:
                print("\nLaissez vide pour conserver la valeur actuelle")
                enreg['nom'] = input(f"Nom [{enreg['nom']}]: ") or enreg['nom']
                enreg['matricule'] = input(f"Matricule [{enreg['matricule']}]: ") or enreg['matricule']
                enreg['service'] = input(f"Service [{enreg['service']}]: ") or enreg['service']
                enreg['poste'] = input(f"Poste [{enreg['poste']}]: ") or enreg['poste']
                enreg['date_embauche'] = input(f"Date embauche [{enreg['date_embauche']}]: ") or enreg['date_embauche']
                
                nouveau_salaire = input(f"Salaire [{enreg['salaire']}]: ")
                enreg['salaire'] = float(nouveau_salaire) if nouveau_salaire else enreg['salaire']
                
                if self.sauvegarder_donnees():
                    print("\n✅ Enregistrement modifié avec succès !")
            else:
                print("\n❌ Aucun enregistrement trouvé avec cet ID.")
        except ValueError:
            print("\n❌ Veuillez entrer un ID valide.")

    def supprimer_enregistrement(self) -> None:
        """Supprime un enregistrement"""
        self.lister_enregistrements()
        if not self.donnees:
            return
            
        try:
            id_suppr = int(input("\nEntrez l'ID de l'enregistrement à supprimer : "))
            for i, enreg in enumerate(self.donnees):
                if enreg['id'] == id_suppr:
                    confirm = input(f"Confirmez la suppression de {enreg['nom']} ? (o/n) : ")
                    if confirm.lower() == 'o':
                        del self.donnees[i]
                        if self.sauvegarder_donnees():
                            print("\n✅ Enregistrement supprimé avec succès !")
                    return
            print("\n❌ Aucun enregistrement trouvé avec cet ID.")
        except ValueError:
            print("\n❌ Veuillez entrer un ID valide.")

    def afficher_statistiques(self) -> None:
        """Affiche des statistiques"""
        if not self.donnees:
            print("\nAucune donnée disponible pour les statistiques.")
            return
            
        print("\n--- Statistiques ---")
        
        # Comptage par service
        services = {}
        salaires = []
        
        for enreg in self.donnees:
            services[enreg['service']] = services.get(enreg['service'], 0) + 1
            salaires.append(enreg['salaire'])
        
        print(f"\nTotal enregistrements : {len(self.donnees)}")
        print(f"Salaire moyen : {sum(salaires)/len(salaires):.2f} €")
        print(f"Salaire max : {max(salaires):.2f} €")
        print(f"Salaire min : {min(salaires):.2f} €")
        
        print("\nRépartition par service :")
        for service, count in services.items():
            print(f"- {service} : {count} employé(s)")

    def executer(self) -> None:
        """Lance l'application"""
        print("Bienvenue dans le système de gestion administrative")
        
        while True:
            self.afficher_menu()
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.ajouter_enregistrement()
            elif choix == "2":
                self.lister_enregistrements()
            elif choix == "3":
                self.rechercher_enregistrement()
            elif choix == "4":
                self.modifier_enregistrement()
            elif choix == "5":
                self.supprimer_enregistrement()
            elif choix == "6":
                self.afficher_statistiques()
            elif choix == "0":
                print("\nMerci d'avoir utilisé le système. Au revoir !")
                break
            else:
                print("\n❌ Choix invalide. Veuillez réessayer.")
            
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    app = GestionAdministrative()
    app.executer()
