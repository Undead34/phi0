"use client";

import { useOne, useUpdate, useCreate } from "@refinedev/core";


export default function IndexPage() {
  const { data, isLoading } = useOne({ resource: "products", id: 123 });
  const { mutate, isLoading: isUpdating } = useUpdate();
  const { mutate: mutateCreate } = useCreate();

  const updatePrice = async () => {
    await mutate({
      resource: "products",
      id: 123,
      values: {
        price: Math.floor(Math.random() * 100),
      },
    });
  };

  const createProduct = async () => {
    await mutateCreate({
      invalidates: ["all"],
      resource: "products",
      values: {
        id: 123,
        name: "Bosch Icon Wiper Blades (Pair)",
        description: "Experience superior all-weather performance with these premium wiper blades. Featuring a patented beam design and advanced rubber compound, they offer exceptional clearing in rain, snow, and sleet.",
        price: 70,
        material: "Rubber, plastic, metal",
        category: {
          "id": 15
        }
      },
    });
  };


  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data) {
    return (
      <div>
        <div>No hay datos disponibles</div>
        <button onClick={createProduct}>Create Product</button>
      </div>
    );
  }

  return (
    <div>
      <div>Product name: {data?.data.name}</div>
      <div>Product price: ${data?.data.price}</div>
      <button onClick={updatePrice}>Update Price</button>
    </div>
  );
}
