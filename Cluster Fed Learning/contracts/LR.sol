// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract LogisticRegressionModel {
    uint256[] public coefs;
    uint256[] public intercepts;

    function setModelParameters(uint256[] memory _coefs, uint256[] memory _intercepts) public {
        delete coefs;
        delete intercepts;
        for (uint i = 0; i < _coefs.length; i++) {
            coefs.push(_coefs[i]);
        }
        for (uint i = 0; i < _intercepts.length; i++) {
            intercepts.push(_intercepts[i]);
        }
    }

    function getModelParameters() public view returns (uint256[] memory, uint256[] memory) {
        return (coefs, intercepts);
    }
}
