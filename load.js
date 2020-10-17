import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

const octokit = new Octokit();

octokit.repos
  .listForOrg({
    org: "facebook",
    type: "public",
  })
  .then(({ data }) => {
  	console.log('ayylmao');
    console.log(data);
  });