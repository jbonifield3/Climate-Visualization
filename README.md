# cse6242-group-project

## Members
| Name                | Email                  |
|---------------------|------------------------|
| James Bonifield     | jbonifield3@gatech.edu |
| Diego Carvallo      | dcarvallo3@gatech.edu  |
| Christopher Comfort | ccomfort3@gatech.edu   |
| Wesley Smith        | wsmith42@gatech.edu    |

## How to work on this repo
Here's a simple workflow adapted from the common [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). The goal is to allow us to edit our code independently without having to spend too much time synchronizing and resolving merge conflicts. 

* All development should be done on a "feature branch", i.e. not `master`.
* "Feature branch" can be loosely defined here. It could be something like `wes-dev`. It's best to avoid long-lived branches, however, because it can be challenging to stay updated with master. An even better example would be `create-chloropleth`, which would only be used while the chloropleth is in development.
* Only changes that are ready for "production" should be moved to `master`.
* When ready to place new changes on `master`:
  1. Ensure that your branch has the most recent version of `master` by performing a `git rebase master` on the feature branch.
    ```
    git pull origin master
    git checkout <feature-branch-name>
    git rebase master
    ```
  2. We will not do pull requests unless we need to. Too much overhead.
  3. Use [`git rebase`](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase) to merge your changes to `master`. `rebase` is preferable to `merge` as merge comments offer little information on what work was done.
    ```
    git checkout master
    git rebase <feature-branch-name>
    ```
  4. Push your changes to remote.
    ```
    git push origin master
    ```
  5. Delete the feature branch and move on to the next one!
