const LogisticRegressionModel = artifacts.require("LogisticRegressionModel");

module.exports = function(deployer) {
  deployer.deploy(LogisticRegressionModel);
};
