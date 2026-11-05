*** Settings ***
Library     ElectionsLibrary


*** Test Cases ***
Election Without District
    Given An Election "without district" With Candidates "Michel, Jerry, Johnny"
    When "Bob" Votes For "Jerry" In "District 1"
    And "Jerry" Votes For "Jerry" In "District 2"
    And "Anna" Votes For "Johnny" In "District 1"
    And "Johnny" Votes For "Johnny" In "District 3"
    And "Matt" Votes For "Donald" In "District 3"
    And "Jess" Votes For "Joe" In "District 1"
    And "Simon" Votes For "" In "District 2"
    And "Carole" Votes For "" In "District 3"
    Then Results Are Verified

Election With Districts
    Given An Election "with districts" With Candidates "Michel, Jerry, Johnny"
    When "Bob" Votes For "Jerry" In "District 1"
    And "Jerry" Votes For "Jerry" In "District 2"
    And "Anna" Votes For "Johnny" In "District 1"
    And "Johnny" Votes For "Johnny" In "District 3"
    And "Matt" Votes For "Donald" In "District 3"
    And "Jess" Votes For "Joe" In "District 1"
    And "July" Votes For "Jerry" In "District 1"
    And "Simon" Votes For "" In "District 2"
    And "Carole" Votes For "" In "District 3"
    Then Results Are Verified
