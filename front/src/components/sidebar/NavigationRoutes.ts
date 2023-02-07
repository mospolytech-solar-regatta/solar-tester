export interface INavigationRoute {
  name: string;
  displayName: string;
  meta: { icon: string };
  children?: INavigationRoute[];
}

export default {
  root: {
    name: "/",
    displayName: "Home"
  },
  routes: [
    {
      name: "dashboard",
      displayName: "Dashboard",
      meta: {
        icon: "vuestic-iconset-dashboard"
      }
    },
    {
      name: "monitor",
      displayName: "Monitor logs",
      meta: {
        icon: "vuestic-iconset-dashboard"
      }
    }
  ] as INavigationRoute[]
};
