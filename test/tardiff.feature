@fixture.workspace
Feature: tardiff

  Scenario: two empty directories
     Given a directory dir1
       And a directory dir2
      When we diff dir1/ and dir2/ into delta/
       And we apply delta/ to dir1/ into restored/
      Then directories dir2/ and restored/ are identical

  Scenario Outline: a file or directory is removed
     Given a test directory dir1
       And a test directory dir2
      When we remove dir2/<path>
       And we diff dir1/ and dir2/ into delta/
       And we apply delta/ to dir1/ into restored/
      Then directories dir2/ and restored/ are identical

    Examples:
      | path         |
      | file         |
      | link         |
      | dir          |
      | dir/file     |
      | dir/link     |
