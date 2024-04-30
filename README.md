# M1if10 - Groupe 16

## Projet d'application web de calcul d'emprunte carbone

### Lien vers la VM de démo

192.168.75.19

### Description

Ce projet consiste à réaliser une application web permettant de calculer l'empreinte carbone d'un utilisateur. Via un questionnaire en ligne, l'utilisateur pourra renseigner ses habitudes de vie et l'application lui donnera un score d'empreinte carbone. Suite aux calculs, différentes statistiques seront affichées à l'utilisateur pour lui permettre de mieux comprendre l'impact de ses habitudes sur l'environnement. L'application permettra également de comparer son score avec celui d'un francais moyen.

### Initialisation du projet et dépendances

Pour initialiser le projet, vous pouvez le clone avec cette adresse: https://forge.univ-lyon1.fr/mif10-groupe-16/m1if10-groupe-16
Le serveur fonctionne grâce au framework Django. Il vous faut un environnement Python avec la version 3.11. Vous pouvez ensuite acquerir les dépendances du projet avec la commande `pip install -r requirements.txt`.

### Lancement du projet

Pour lancer le projet en local, il suffit de se situer dans le 1er dossier backend et dans un environnement anaconda, il faudra ensuite lancer la commande `python manage.py runserver`.

### Build du projet

Lors du build du projet, les dossiers backend et frontend sont envoyés sur la VM, le serveur gunicorn de la vm se met à jour et se relance.

### Sonar

Sonar est un outil de qualité de code. Pour vérifier que notre projet est conforme aux normes de qualité, nous utilisons le serveur Sonar de la fac.
Pour lancer un test manuellement vous pouvez lancer la commande :

```shell
sudo ./sonar/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner \
     -Dproject.settings=sonar/sonar-project.properties   \
     -Dsonar.token=<votreToken>
```

Sonar est appele automatiquement lors de chaque push sur le serveur git.

### test
Des tests ont été déployé sur le projet, vous pouvez les lancer avec :
```bash
python3 manager test
```
En plus de cela le requirements.txt vous install un outils de coverage :
```py
coverage run --source='.' manage.py test --keepdb
coverage xml -o ../coverage_report/coverage.xml 
```
