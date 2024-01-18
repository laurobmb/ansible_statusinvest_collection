# Ansible Collection - laurobmb.statusinvest

Documentation for the collection.

### Galaxy collection build
> ansible-galaxy collection build
### Galaxy collection install from file
> ansible-galaxy collection install laurobmb-statusinvest-1.0.0.tar.gz
### Galaxy collection install from git
> ansible-galaxy collection install git+https://github.com/laurobmb/ansible_statusinvest_collection.git,main

> ansible-galaxy collection install laurobmb-statusinvest-1.0.4.tar.gz -p collections/

### Playbook sample
    ---
    - name: STATUSINVEST
      hosts: localhost
      vars:
        acoes: "bbas3"
        fundos: "vghf11"
      tasks:
        - name: Import role
          ansible.builtin.import_role:
            name: laurobmb.statusinvest.getdata
