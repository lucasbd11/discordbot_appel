# discordbot_appel
Avec les problèmes de confinement une bonne partie des cours se font maintenant en ligne sur de diverses platformes. Discord fait parti
de ces plaformes. Ce bot utilisable sur discord permet d'automatiser l'appel pour savoir quels sont les utilisateurs manquants dans un salon
vocal.
# Commande:
!appel <rôle>

Cette commande permet de voir les personnes possédants un certain rôle qui ne sont pas dans le salon vocal où la personne a exécuté la commande. L'utilisateur exécutant la commande doit avoir le rôle "professeur"
il est possible de ne rien passer en paramètre, ou de passer plusieurs rôles en paramètres

# Exemple:
!appel
Tous les membres n'ayant pas le rôle "professeur" vont être ciblés

!appel PCSI2
Tous les membres avec au moins lr rôle "PCSI2" vont être ciblés.

!appel TerminaleS2,ISN
Seuls les membres avec au moins les 2 rôles "TerminaleS2" et "ISN" vont être ciblés.
