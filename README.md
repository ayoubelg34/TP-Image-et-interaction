# Cahier des charges et spécifications du projet
1. Introduction
- Le projet consiste à développer une version interactive du jeu classique Pong, utilisant Python et
OpenCV. Les joueurs contrôleront les raquettes à l’aide de leurs mains, détectées par une caméra.
Le projet inclut un affichage en temps réel, une gestion fluide des interactions et des fonctionnalités
bonus comme des obstacles ou un mode multijoueur réseau.

2. Objectifs principaux
-Développer un jeu fonctionnel et interactif basé sur le contrôle des raquettes avec les
mouvements des mains.
-Offrir une expérience utilisateur fluide, avec un affichage en temps réel via OpenCV.
- Intégrer un système de score et des interactions conformes aux mécaniques de jeu de Pong.

3.Objectifs secondaires (Bonus)
- Ajouter des obstacles dynamiques pour augmenter la difficulté.
- Implémenter un mode multijoueur réseau avec deux caméras.
- Publier un leaderboard en ligne avec statistiques des joueurs.

4. Contraintes techniques
- Langage : Utilisation exclusive de Python
- Technologies : OpenCV pour la gestion du flux vidéo et la détection des mains.
- Matériel : Flux vidéo géré par une Raspberry Pi et une caméra USB ou intégrée.
- Affichage : Temps réel, avec une fréquence d’images stable (FPS).
- Interaction : Contrôler les raquettes via la détection des mouvements des mains.
- Livrables : Respect des délais pour les différentes étapes du projet.

5. Spécifications fonctionnelles
- Détection des mains
• Suivi des mains des deux joueurs en temps réel.
• Association de la position des mains aux raquettes du jeu.
- Mécanique de jeu• Mouvement continu de la balle selon les règles classiques de Pong.
• Rebond de la balle sur les murs et les raquettes.
• Gestion des collisions entre la balle et les limites du terrain.
- Affichage et Score
• Terrain, raquettes et balle affichés dynamiquement.
• Calcul et affichage des scores en temps réel.

6. Fonctionnalités avancées (Bonus)
- Obstacles dynamiques
- Leaderboard (High score).

7. Conclusion
- Ce projet vise à mêler interaction utilisateur et développement algorithmique en utilisant la vision
par ordinateur. Grâce à l’implémentation des fonctionnalités minimales et avancées, ce jeu offrira
une expérience innovante et immersive tout en respectant les contraintes imposées.
