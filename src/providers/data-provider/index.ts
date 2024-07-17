"use client";

import type { DataProvider } from "@refinedev/core";

import { doc, getDoc, updateDoc, setDoc } from "firebase/firestore";
import { db, firebaseConfig } from "./firebase";

export const dataProvider: DataProvider = {
    getOne: async ({ resource, id, meta }) => {
        const response = await getDoc(doc(db, resource, id.toString()));

        if (!response.exists()) throw new Error(`Document with ID ${id} in resource ${resource} does not exist`);

        const data = { data: { id: response.id, ...response.data() } } as any;

        return data;
    },
    update: async ({ resource, id, variables }) => {
        try {
            await updateDoc(doc(db, resource, id.toString()), variables as any);

            return { data: null } as any;
        } catch (error) {
            throw new Error(`An error occurred when trying to update the data in the document with ID ${id} in the resource ${resource}.`);
        }
    },
    create: async ({ resource, variables, meta }) => {
        try {
            const id: any = (variables as any).id.toString();

            await setDoc(doc(db, resource, id), variables as any);

            return { data: null } as any;
        } catch (error) {
            console.log(error);
            throw new Error(`An error occurred while trying to create the document with the data ${variables} in the resource ${resource}.`);
        }
    },
    getApiUrl: () => firebaseConfig.authDomain as string,
    getList: () => { throw new Error("Not implemented"); },
    deleteOne: () => { throw new Error("Not implemented"); },
};
