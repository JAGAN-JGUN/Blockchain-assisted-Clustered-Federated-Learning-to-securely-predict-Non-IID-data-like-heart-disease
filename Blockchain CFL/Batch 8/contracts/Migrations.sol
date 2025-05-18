// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LogisticRegressionModel {
    int256[13] public coefs;
    int256 public intercepts;
    constructor() public {
        for (uint i = 0; i < 13; i++) {
            coefs[i] = 0;
        }
        intercepts = 0;
    }

    function setModelParameters(int256[13] memory _coefs, int256 _intercepts) public {
        for (uint i = 0; i < 13; i++) {
            coefs[i] = _coefs[i];
        }
        intercepts = _intercepts;
    }

    function getModelParameters() public view returns (int256[13] memory, int256) {
        return (coefs, intercepts);
    }
}
