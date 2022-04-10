@fixture.workspace
Feature: tardiff can diff directories

  Scenario: compare two directories
     Given a directory a
       And a directory b
      When we diff a and b into c
      Then c is empty
