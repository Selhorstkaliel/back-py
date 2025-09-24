import create from "zustand";

export const useFilters = create(set => ({
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1,
  half: 1,
  setYear: year => set({ year }),
  setMonth: month => set({ month }),
  setHalf: half => set({ half }),
}));