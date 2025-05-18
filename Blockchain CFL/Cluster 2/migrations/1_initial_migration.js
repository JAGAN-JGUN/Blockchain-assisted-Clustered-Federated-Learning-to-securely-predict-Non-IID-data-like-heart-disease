const Migrations = artifacts.require("LogisticRegressionModel");

module.exports = function(deployer,network,accounts) {
  deployer.deploy(Migrations, {from: accounts[13]});
};