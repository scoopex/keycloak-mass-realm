
# About

I created this hacking script to demonstrate a problem for a bugreport.
See: https://github.com/keycloak/keycloak/issues/20453

# Setup a test instance


* Download Keycloak
* Start it
  ```
  export KEYCLOAK_ADMIN=admin
  export KEYCLOAK_ADMIN_PASSWORD=nimda
  export KEYCLOAK_DIR="$PWD"
  cd bin
  ./kc.sh  start-dev
  ```
* Stop it


# Perform a mass import


* Generate Files
  ```
  git clone https://gitlab.com/scoopex/keycloak-mass-realm.git
  cd keycloak-mass-realm
  ./generate -n 400
  REALM_DIR="$PWD/generated"
  ```
* Import them
  see: https://www.keycloak.org/server/importExport
  Unfortunately the import takes some time because "--dir $REALM\_DIR" option does not import the 
  realms in a single step as expected.
  ```
  cd $KEYCLOAK_DIR/bin
  for file in $REALM_DIR/*.json; do 
    echo "$file"; 
    ./kc.sh import --file $file; 
  done
  ```
* Start it
  ```
  ./kc.sh  start-dev
  ```
