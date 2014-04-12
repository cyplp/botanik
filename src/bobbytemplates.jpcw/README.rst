.. contents::

Introduction
============

**mr.bobby** templates : http://mrbobby.readthedocs.org/en/latest/

+ basic_namespace : provide a zopeskel-like (basic_namespace) template


Installation
---------------

::
 
  - git clone -b master https://github.com/jpcw/mr.bobby.git
  - cd mr.bobby
  - python setup.py install
  - cd ../
  - git clone -b master https://github.com/jpcw/bobbyplugins.jpcw.git
  - cd bobbyplugins.jpcw
  - python setup.py install
  - git clone -b master https://github.com/jpcw/bobbytemplates.jpcw.git
  - cd ../bobbytemplates.jpcw/
  - python setup.py develop
  - easy_install . bobbytemplates.jpcw[test]
  

Templates
------------

basic_namespace
++++++++++++++++++

:: 
   
 --> Namespace Package Name [paulla]:
 --> Package Name [paste]:
 --> Description:
 --> Author: 
 --> Author Email:
 --> Keywords ['']:
 --> Project URL ['']: 
 --> Project License [BSD|GPL] [BSD]:
 --> Zip-Safe [true/false] [false]:

pkg_ns (namespace) and pkg_project (package name) are guessed from -O option 

::
 
 mrbobby -O paulla.paste bobbytemplates.jpcw:basic_namespace

return ::
 
 --> Namespace Package Name [paulla]:
 --> Package Name [paste]:


Tests
=====

bobbytemplates.jpcw is continuously 

+ tested on Travis |travisstatus|_ 

+ coverage tracked on coveralls.io |coveralls|_.

.. |travisstatus| image:: https://api.travis-ci.org/jpcw/bobbytemplates.jpcw.png
.. _travisstatus:  http://travis-ci.org/jpcw/bobbytemplates.jpcw


.. |coveralls| image:: https://coveralls.io/repos/jpcw/bobbytemplates.jpcw/badge.png
.. _coveralls: https://coveralls.io/r/jpcw/bobbytemplates.jpcw