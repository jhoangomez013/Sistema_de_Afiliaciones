import { NgModule } from "@angular/core";
import { MatButton } from "@angular/material/button";
import { MatCard } from "@angular/material/card";
import { MatIcon } from "@angular/material/icon";
import { MatToolbar } from "@angular/material/toolbar";
import { MatFormFieldModule } from "@angular/material/form-field";

const materialModules = [
    MatToolbar,
    MatButton,
    MatCard,
    MatIcon,
    MatFormFieldModule
];

@NgModule({
    imports: [...materialModules],
    exports: [...materialModules],
    providers: []
})
export  class MaterialModule { }