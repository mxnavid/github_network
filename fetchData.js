import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

  const octokit = new Octokit();

// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
octokit.repos
  .listForOrg({
    org: "facebook",
    type: "public",
  })
  .then(({ data }) => {
  	console.log('ayylmao');
    console.log(data);
  });