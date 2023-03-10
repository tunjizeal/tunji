/** Don't use anything here for new components */
import React, {FC} from 'react';
import {
  Params,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
  Location,
  NavigateFunction,
} from 'react-router-dom';

// https://stackoverflow.com/a/70754791/443457
const getRoutePath = (location: Location, params: Params): string => {
  const {pathname} = location;

  if (!Object.keys(params).length) {
    return pathname; // we don't need to replace anything
  }

  let path = pathname;
  Object.entries(params).forEach(([paramName, paramValue]) => {
    if (paramValue) {
      path = path.replace(paramValue, `:${paramName}`);
    }
  });
  return path;
};

interface RouterProp {
  location: Location;
  navigate: NavigateFunction;
  params: Readonly<Params<string>>;
  searchParams: URLSearchParams; // Replaces props.location.query
  path: string; // Replaces props.route.path
}

export interface WithRouterProps {
  router: RouterProp;
  params: Readonly<Params<string>>; // Defined as props twice for compat!

}

/**
 * This is for class based components, which cannot use hooks
 * Attempts to mimic both react router 3 and 5!
 * https://v5.reactrouter.com/web/api/withRouter
 * Use hooks instead when possible
 */
export function withRouter(Component: FC | typeof React.Component) {
  function ComponentWithRouterProp(props: any) {
    const location = useLocation();
    const navigate = useNavigate();
    const [searchParams, _] = useSearchParams();
    const params = useParams();
    const path = getRoutePath(location, params);
    const router: RouterProp = {location, navigate, params, searchParams, path};
    return <Component {...props} params={params} router={router} />;
  }

  return ComponentWithRouterProp;
}

function getCurrentRoute() {
  return location.hash.split('#')[1] || '';
}

/**
 * Reimplementation of router v3 isActive
 */
export function routerIsActive(route: string) {
  return getCurrentRoute().startsWith(route);
}

export function routerGetAssetId() {
  const current = getCurrentRoute();
  if (current) {
    const routeParts = current.split('/');
    if (routeParts[1] === 'forms') {
      return routeParts[2];
    } else if (routeParts[1] === 'library') {
      return routeParts[3];
    }
  }
  return null;
}
