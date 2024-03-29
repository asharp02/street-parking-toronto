import Checkbox from "./Checkbox.jsx";
import React, { useState } from 'react';

function BylawToggle({ toggleHandler, isNPChecked, isRPChecked, setIsNPChecked, setIsRPChecked }) {
    const toggleBylawMarkers = (isNoParkingMarkers) => {
        if (isNoParkingMarkers){
            toggleHandler(isNoParkingMarkers, isNPChecked);
            setIsNPChecked(!isNPChecked);
        } else {
            toggleHandler(isNoParkingMarkers, isRPChecked);
            setIsRPChecked(!isRPChecked);
        }
    }

    return (
        <div className="toggleSidebar">
            <Checkbox 
                index="noParking"
                label="No Parking" 
                checkHandler={() => toggleBylawMarkers(true)}
                checkedStatus={isNPChecked}
            />
            <Checkbox 
                index="validParking"
                label="Free Parking" 
                checkHandler={() => toggleBylawMarkers(false)}
                checkedStatus={isRPChecked}
            />
        </div>
    )
}

export default BylawToggle;