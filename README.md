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
        acoes: "itsa4"
        fundos: "vghf11"
      tasks:
        - name: Import role
          ansible.builtin.import_role:
            name: laurobmb.statusinvest.getdata
    
        - name: Get result
          laurobmb.statusinvest.statusinvest:
            statusinvest_acoes: "{{ acoes }}"
            statusinvest_fundos: "{{ fundos }}"
          register: greeting
    
        - name: Debug
          ansible.builtin.debug:
            msg: "{{ greeting }}"
